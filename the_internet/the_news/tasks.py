from typing import Dict

from celery import shared_task
from celery.schedules import crontab


from the_internet import celery_app

@celery_app.task(name="debug-task")
def debug_task(data):
    print(f'data: {data!r}')

celery_app.conf.beat_schedule['debug-task'] = {
        'task': 'debug-task',
        'schedule': crontab(hour=1),
        'args': [{"foo": "bar"}]
    }