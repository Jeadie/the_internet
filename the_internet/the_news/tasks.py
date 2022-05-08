import json

from celery.schedules import crontab
from django.utils.timezone import make_aware

from the_news.models import InternetLocation, InternetNews, InternetLocationCategory
from the_news.content_providers import get_all_internet_content, RedditChannelContentProvider, ProductHuntContentProvider, HackerNewsContentProvider, IndieHackerContentProvider

from the_internet import celery_app

celery_app.conf.beat_schedule['add_internet_news'] = {
        'task': 'add_internet_news',
        'schedule': crontab(hour=1),
        'args': []
    }

@celery_app.task(name="add_internet_news")
def add_internet_news() -> None:
    """Async task to create InternetNews from various content providers. """
    news = get_all_internet_content(
        [RedditChannelContentProvider("technology"), ProductHuntContentProvider(), HackerNewsContentProvider(), IndieHackerContentProvider()]
    )
    # TODO: use and create bulk create
    for n in news:
        location, _ = InternetLocation.objects.get_or_create(location_type=n.content_type)
        internet_news, _ = InternetNews.objects.get_or_create(id= n.id, defaults = {
                "timestamp" : make_aware(n.timestamp),
                "title" : n.title,
                "url" : n.url,
                "description": n.content.get("description", None),
                "location": location,
                "additional_fields" : json.dumps(n.content),
                "upvotes": n.content.get("upvotes", 0),
                "comments": n.content.get("comments", 0)
            }
        )
        # Add location subtypes (cannot add directly since many-to-many)
        if n.subtype:
            category, _  = InternetLocationCategory.objects.get_or_create(location=location, category_name=n.subtype)
            internet_news.sub_category.set([category])
