import json
from typing import List

from django.shortcuts import render
from django.http import HttpRequest
from rest_framework import permissions, serializers, viewsets
from rest_framework.request import Request as DRFRequest

from .models import InternetLocation, InternetNews
from the_internet import settings
from .content_providers import InternetContent

class InternetNewsListSerializer(serializers.ListSerializer):
    pass

class InternetNewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InternetNews
        list_serializer_class = InternetNewsListSerializer
        fields = '__all__'

class InternetNewsViewSet(viewsets.ModelViewSet):
    queryset = InternetNews.objects.all()
    serializer_class = InternetNewsSerializer
    permission_classes = [permissions.IsAuthenticated]

class InternetLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InternetLocation
        fields = '__all__'

class InternetLocationViewSet(viewsets.ModelViewSet):
    queryset = InternetLocation.objects.all()
    serializer_class = InternetLocationSerializer
    permission_classes = [permissions.IsAuthenticated]




def add_internet_news(news: List[InternetContent]) -> None:
    
    # TODO: use and create bulk create 
    for c in news:
        request = HttpRequest()
        request.method = 'POST'
        request.META = {
            'SERVER_NAME': settings.ALLOWED_HOSTS[0],
            'SERVER_PORT': 443
        }
        drf_request = DRFRequest(request)

        # If your API need user has access permission,
        # you should handle for getting the value of
        # user_has_access_permission before
        # E.g. below
        # drf_request.user = user_has_access_permission
        try:
            InternetNews.objects.get_or_create(id= c.id,
                defaults = {
                    "timestamp" : c.timestamp,
                    "title" : c.title,
                    "url" : c.url,
                    "additional_fields" : json.dumps(c.content)  
                }
            )
        except Exception as e:
            print(f'Error: {e}')
