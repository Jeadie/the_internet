from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class InternetLocation(models.Model):
    """
    A location on the internet where InternetNews can be retrieved from.
    """
    location_type = models.CharField(
        primary_key=True,
        max_length=128
    )

class InternetLocationCategory(models.Model):
    """ A division of a InternetLocation into possible subcategories of interest."""
    location = models.ForeignKey(InternetLocation, on_delete=models.CASCADE)
    category_name = models.CharField("Category Name", max_length=128)


class InternetNews(models.Model):
    """
    A single piece of content from the internet.
    """
    id = models.CharField(primary_key=True, max_length=128)
    timestamp = models.DateTimeField()
    title = models.CharField(max_length=512)
    url = models.URLField()

    location = models.ForeignKey(InternetLocation, null=True, on_delete=models.SET_NULL)
    sub_category = models.ManyToManyField(InternetLocationCategory, blank=True)

    description = models.TextField(max_length=1024, null=True, blank=True)
    image_src = models.URLField(null=True, blank=True)

    upvotes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    additional_fields = models.JSONField()

class UserNewsProfile(models.Model):
    """A users relation/profile to the_news"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_internet_location_categories = models.ManyToManyField(InternetLocationCategory, blank=True)

