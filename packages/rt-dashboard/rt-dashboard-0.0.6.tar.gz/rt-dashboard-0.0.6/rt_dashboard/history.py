import datetime
from collections import defaultdict

import pytz

from redis_tasks.conf import settings
from redis_tasks.registries import (
    failed_task_registry, finished_task_registry, worker_registry)
from redis_tasks.task import Task
from redis_tasks.utils import utcnow
from redis_tasks.worker import Worker


def jsdate(d):
    t = list(d.timetuple()[:6])
    # In js, January is 0
    t[1] -= 1
    return 'new Date{}'.format(tuple(t))


def task_tooltip(t):
    return f'''
    <b>{t.description}</b><br>
    {t.started_at:%H:%M:%S} - {t.ended_at:%H:%M:%S}<br>
    Duration: {t.ended_at - t.started_at}<br>
    <i>{t.status}</i><br>
    '''


def get_history_context():
    max_finished_tasks = 5000
    max_failed_tasks = 1000
    finished_tasks = finished_task_registry.get_tasks(-max_finished_tasks, -1)
    failed_tasks = failed_task_registry.get_tasks(-max_failed_tasks, -1)
    if len(finished_tasks) == max_finished_tasks:
        failed_tasks = [t for t in failed_tasks
                        if t.ended_at >= finished_tasks[0].ended_at]
    if len(failed_tasks) == max_failed_tasks:
        finished_tasks = [t for t in finished_tasks
                          if t.ended_at >= failed_tasks[0].ended_at]

    now = utcnow()
    running_tasks = []
    for wid, tid in worker_registry.get_running_tasks().items():
        task = Task.fetch(tid)
        task.ended_at = now
        task.running_on = Worker.fetch(wid).description
        running_tasks.append(task)

    tasks = failed_tasks + finished_tasks + running_tasks
    tasks.sort(key=lambda t: t.started_at)

    by_func = defaultdict(list)
    for t in tasks:
        by_func[t.func_name].append(t)

    # reconstruct worker-mapping
    for group in by_func.values():
        workers = []
        for task in sorted(group, key=lambda t: t.started_at):
            workers = [
                None if not t or t.ended_at <= task.started_at else t
                for t in workers
            ]
            try:
                task.worker = workers.index(None)
                workers[task.worker] = task
            except ValueError:
                task.worker = len(workers)
                workers.append(task)

    groups = sorted(
        by_func.values(),
        key=lambda group_tasks: (
            min(t.started_at.timetuple()[3:] for t in group_tasks),
            max(t.ended_at - t.started_at for t in group_tasks)
        ))
    groups = ",\n".join(
        "{{id: '{0}', content: '{0}', order: {1}}}".format(group_tasks[0].func_name, i)
        for i, group_tasks in enumerate(groups))

    collapsed_groups = {k for k, v in by_func.items()
                        if len(v) / len(tasks) < 0.02}

    tz = pytz.timezone(settings.TIMEZONE)
    rows = []
    for t in tasks:
        t.started_at = t.started_at.astimezone(tz)
        t.ended_at = t.ended_at.astimezone(tz)
        keys = {
            'group': t.func_name,
            'subgroup': t.worker,
            'start': t.started_at,
            'title': task_tooltip(t),
        }
        if hasattr(t, 'running_on'):
            keys.update({
                'end': t.ended_at,
                'type': 'range',
                'content': t.running_on,
            })
        elif (t.func_name not in collapsed_groups or
                (t.ended_at - t.started_at) > datetime.timedelta(minutes=1)):
            keys.update({
                'end': t.ended_at,
                'type': 'range',
                'content': '[{}]'.format(t.ended_at - t.started_at),
            })
        else:
            keys.update({
                'type': 'point',
                'content': t.started_at.strftime('%H:%M:%S'),
            })

        if t.status == 'failed':
            keys['style'] = 'border-color: {0}; background-color: {0}'.format('#E69089')
        elif t.status == 'running':
            keys['style'] = 'border-color: {0}; background-color: {0}'.format('#D5F6D7')

        keys = {k: jsdate(v) if isinstance(v, datetime.datetime) else repr(v)
                for k, v in keys.items()}
        rows.append('{' + ','.join('{}: {}'.format(k, v) for k, v in keys.items()) + '}')
    rowtext = ",\n".join(rows)

    return dict(rows=rowtext, groups=groups)
