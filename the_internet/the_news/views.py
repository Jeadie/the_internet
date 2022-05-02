import json
from typing import List

from django.shortcuts import render
from django.http import HttpRequest
from django.views import generic
from rest_framework import permissions, serializers, viewsets
from rest_framework.request import Request as DRFRequest

from .models import InternetLocation, InternetNews
from the_internet import settings
from .content_providers import InternetContent
from .serializers import InternetNewsSerializer, InternetLocationSerializer


class InternetNewsIndexView(generic.ListView):
    """UI for the list view of internet news"""
    template_name = 'templates/internet_news.html'
    context_object_name = 'latest_news_list'

    def get_queryset(self):
        return InternetNews.objects.order_by('-timestamp')


class InternetNewsRestViewSet(viewsets.ModelViewSet):
    queryset = InternetNews.objects.all()
    serializer_class = InternetNewsSerializer
    permission_classes = [permissions.IsAuthenticated]

class InternetLocationRestViewSet(viewsets.ModelViewSet):
    queryset = InternetLocation.objects.all()
    serializer_class = InternetLocationSerializer
    permission_classes = [permissions.IsAuthenticated]