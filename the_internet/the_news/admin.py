from django.contrib import admin

from the_news.models import InternetLocation, InternetNews

admin.site.register(InternetNews)
admin.site.register(InternetLocation)