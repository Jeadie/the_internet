from django.conf import settings
from django.urls import include, path
from rest_framework import routers

from .views import InternetLocationRestViewSet, InternetNewsRestViewSet, InternetNewsIndexView

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()
    
router.register("news", InternetNewsRestViewSet)
router.register("locations", InternetLocationRestViewSet)

urlpatterns = [
    path('', InternetNewsIndexView.as_view(), name='news_page'),
    path("", include(router.urls)),
]