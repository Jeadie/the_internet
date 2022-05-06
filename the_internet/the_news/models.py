from django.db import models
from django.utils.translation import gettext_lazy as _

class ContentLocation(models.TextChoices):
    """InternetLocation names integrated into the_news"""
    HACKER_NEWS_NEWS = 'HN_N', _('Hacker News')
    INDIE_HACKERS_POPULAR = 'IH_P', _('Indie Hackers')
    PRODUCT_HUNT_TODAY = "PH_T", _("Product Hunt")
    REDDIT_CHANNEL_TODAY = "R_C_T", ("Reddit")

class InternetLocation(models.Model):
    """
    A location on the internet where InternetNews can be retrieved from.
    """
    location_type = models.CharField(
        primary_key=True,
        choices=ContentLocation.choices,
        max_length=128
    )

class InternetNews(models.Model):
    """
    A single piece of content from the internet.
    """
    id = models.CharField(primary_key=True, max_length=128)
    timestamp = models.DateTimeField()
    title = models.CharField(max_length=512)
    url = models.URLField()
    location = models.ForeignKey(InternetLocation, null=True, on_delete=models.SET_NULL)

    description = models.TextField(max_length=1024, null=True, blank=True)
    image_src = models.URLField(null=True, blank=True)

    upvotes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    additional_fields = models.JSONField()
