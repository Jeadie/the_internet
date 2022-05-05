from django.conf import settings
from django.urls import include, path, re_path
from rest_framework import routers

from .views import InternetLocationRestViewSet, InternetNewsRestViewSet, InternetNewsIndexView

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()
    
router.register("news", InternetNewsRestViewSet)
router.register("locations", InternetLocationRestViewSet)

urlpatterns = [
    re_path('^(?P<week>[0-9]{1,2})', InternetNewsIndexView.as_view(), name='news_week'),
    re_path(f'^(?P<month>({"|".join(InternetNewsIndexView.allowed_url_months)}))/$', InternetNewsIndexView.as_view(), name='news_month'),
    re_path(f'^(?P<month>({"|".join(InternetNewsIndexView.allowed_url_months)}))/' + '(?P<day>[0-9]{1,2})/$', InternetNewsIndexView.as_view(), name='news_day'),
    path('', InternetNewsIndexView.as_view(), name='news_page'),
    path("", include(router.urls)),
]