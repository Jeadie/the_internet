from typing import Dict, List

from celery import shared_task
from celery.schedules import crontab

from the_internet import celery_app
from the_news import views
from the_news.content_providers import get_internet_content, InternetContent


@celery_app.task(name="debug-task")
def debug_task(data):
    print(f'data: {data!r}')

celery_app.conf.beat_schedule['debug-task'] = {
        'task': 'debug-task',
        'schedule': crontab(hour=1),
        'args': [{"foo": "bar"}]
    }
celery_app.conf.beat_schedule['add_internet_news'] = {
        'task': 'add_internet_news',
        'schedule': crontab(hour=1),
        'args': []
    }

@celery_app.task(name="add_internet_news")
def add_internet_news() -> None:
    """
    Async task to create InternetNews from various content providers.
    """
    news = get_internet_content()
    views.add_internet_news(news)
