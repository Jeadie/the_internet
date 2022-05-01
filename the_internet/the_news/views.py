from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions, serializers, viewsets

from .models import InternetLocation, InternetNews


def index(request):
    return HttpResponse("Hello, world. You're at the news.")


class InternetNewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InternetNews
        fields = ['id', 'timestamp', 'title', 'url', 'location', 'additional_fields']

class InternetNewsViewSet(viewsets.ModelViewSet):
    queryset = InternetNews.objects.all()
    serializer_class = InternetNewsSerializer
    permission_classes = [permissions.IsAuthenticated]


class InternetLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InternetLocation
        fields = ['location_type']

class InternetLocationViewSet(viewsets.ModelViewSet):
    queryset = InternetLocation.objects.all()
    serializer_class = InternetLocationSerializer
    permission_classes = [permissions.IsAuthenticated]