from django.urls import include, path
from rest_framework import routers

from .views import InternetLocationViewSet, InternetNewsViewSet

router = routers.DefaultRouter()
router.register("", InternetNewsViewSet)
router.register("locations", InternetLocationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]