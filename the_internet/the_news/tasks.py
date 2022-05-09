import json

from celery.schedules import crontab
from django.utils.timezone import make_aware

from the_news.models import InternetLocation, InternetNews, InternetLocationCategory
from the_news.content_providers import get_all_internet_content, AFRInternetContentProvider, RedditChannelContentProvider, ProductHuntContentProvider, HackerNewsContentProvider, IndieHackerContentProvider

from the_internet import celery_app


providers = [RedditChannelContentProvider("technology"), ProductHuntContentProvider(), HackerNewsContentProvider(), IndieHackerContentProvider(), AFRInternetContentProvider("policy")]
provider_map = dict([
    (f"run-content-provider-{p.get_content_id()}-{p.get_content_subtype()}", p) for p in providers
    ])

for k in provider_map.keys():
    celery_app.conf.beat_schedule[k] = {
        'task': "add_internet_news",
        'schedule': crontab(hour=1),
        'args': [k,]
    }


@celery_app.task(name="add_internet_news")
def add_internet_news(provider_key: str) -> None:
    """Async task to create InternetNews from various content providers. """

    news = get_all_internet_content([provider_map[provider_key]])

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
