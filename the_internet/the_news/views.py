from datetime import datetime, timedelta
import json
from typing import List

from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import QuerySet
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

    url_month_mapping = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12
    } + dict(
        [(str(i), i) for i in range(1,13)]
    ) + dict(
        [(f"0{i}", i) for i in range(1,10)]
    )


    def get_time_filtered_queryset(self) -> QuerySet:
        month, week, day = self.kwargs.get("month"), self.kwargs.get("week"), self.kwargs.get("day")
        if week and not month: 
            # news_week url
            start = datetime.strptime(f"{datetime.now().year} {week} 1", "%Y %W %w"),
            return InternetNews.objects.filter(timestamp__range=(start, start + timedelta(day=7)))

        elif month and day:
            # news_day url 
            start = datetime.strptime(f"{datetime.now().year} {month} {day}", "%Y %m %d")
            return InternetNews.objects.filter(timestamp__range=(start, start + timedelta(day=1)))
        elif month:
            # news_month url
            start = datetime.strptime(f"{datetime.now().year} {month} 1", "%Y %m %d")
            return InternetNews.objects.filter(timestamp__range=(start, start + timedelta(month=1)))
        else:
            # news_page url
            return InternetNews.objects.all()


    def get_queryset(self):
        qs = self.get_time_filtered_queryset()

        # Random order queryset
        return qs.order_by('?')


class InternetNewsRestViewSet(viewsets.ModelViewSet):
    queryset = InternetNews.objects.all()
    serializer_class = InternetNewsSerializer
    permission_classes = [permissions.IsAuthenticated]

class InternetLocationRestViewSet(viewsets.ModelViewSet):
    queryset = InternetLocation.objects.all()
    serializer_class = InternetLocationSerializer
    permission_classes = [permissions.IsAuthenticated]