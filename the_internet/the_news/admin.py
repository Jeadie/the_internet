from django.contrib import admin

from the_news.models import InternetLocation, InternetNews, InternetLocationCategory


admin.site.register(InternetNews)
admin.site.register(InternetLocation)
admin.site.register(InternetLocationCategory)