from django.conf import settings
from django.urls import include, path
from rest_framework import routers

from .views import InternetLocationViewSet, InternetNewsViewSet

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()
    
router.register("news", InternetNewsViewSet)
router.register("locations", InternetLocationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]