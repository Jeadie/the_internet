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

class InternetLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InternetLocation
        fields = '__all__'
