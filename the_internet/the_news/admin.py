from django.contrib import admin

from the_news.models import InternetLocation, InternetContent

admin.site.register(InternetContent)
admin.site.register(InternetLocation)