import json

from celery.schedules import crontab
from django.utils.timezone import make_aware

from the_internet import celery_app
from the_news.content_providers import get_internet_content

from .models import InternetLocation, InternetNews


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
    # TODO: use and create bulk create 
    for c in news:
        try:
            InternetNews.objects.get_or_create(id= c.id,
                defaults = {
                    "timestamp" : make_aware(c.timestamp),
                    "title" : c.title,
                    "url" : c.url,
                    "description": c.content.get("description", None),
                    "location": InternetLocation.objects.get_or_create(location_type=c.content_type)[0],
                    "additional_fields" : json.dumps(c.content),
                    "upvotes": c.content.get("upvotes", 0),
                    "comments": c.content.get("comments", 0)
                }
            )

        except Exception as e:
            print(f'Error: {e}')
