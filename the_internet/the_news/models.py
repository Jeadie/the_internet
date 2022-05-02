from django.db import models
from django.utils.translation import gettext_lazy as _

class ContentLocation(models.TextChoices):
    HACKER_NEWS_NEWS = 'HN_N', _('Hacker News')
    INDIE_HACKERS_POPULAR = 'IH_P', _('Indie Hackers')

class InternetLocation(models.Model):
    location_type = models.CharField(
        primary_key=True,
        choices=ContentLocation.choices,
        max_length=128
    )

class InternetNews(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    timestamp = models.DateTimeField()
    title = models.CharField(max_length=512)
    url = models.URLField()
    location = models.ForeignKey(InternetLocation, null=True, on_delete=models.SET_NULL)
    additional_fields = models.JSONField()
