from django.db import models

class InternetLocation(models.Model):

    class ContentLocation(models.TextChoices):
        HACKER_NEWS_NEWS = 'HN_N', _('HackerNews_News')
        INDIE_HACKERS_POPULAR = 'IH_P', _('IndieHacker_PopularPosts')

    location_type = models.CharField(
        primary_key=True,
        choices=ContentLocation.choices,
    )

class InternetContent(models.Model):
    id = models.CharField(primary_key=True)
    timestamp = models.DateTimeField()
    title = models.CharField()
    url = models.URLField()
    location = models.ForeignKey(InternetLocation, on_delete=models.SET_NULL)
    additional_fields = models.JSONField()