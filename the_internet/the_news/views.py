from datetime import datetime, timedelta

from django.db.models import QuerySet
from django.views import generic
from rest_framework import permissions, viewsets

from the_news.models import InternetLocation, InternetNews
from .serializers import InternetNewsSerializer, InternetLocationSerializer


class InternetNewsIndexView(generic.ListView):
    """UI for the list view of internet news"""
    template_name = 'templates/internet_news.html'
    context_object_name = 'latest_news_list'

    url_month_mapping = {**{
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
    }, **dict(
        [(str(i), i) for i in range(1,13)]
    ), **dict(
        [(f"0{i}", i) for i in range(1,10)]
    )}

    allowed_url_months = list(url_month_mapping.keys())

    def get_time_filtered_queryset(self) -> QuerySet:
        """ Creates a queryset, filtered by timestamp (base on the url parameter options/url view). Options are:
            1. news_week: Week of the year, 1-52
            2. news_day: single, specific day
            3. news_month: A whole month.
            If no **kwargs are present to create one of the above options, queryset contains all InternetNews.
        """
        month, week, day = self.kwargs.get("month"), self.kwargs.get("week"), self.kwargs.get("day")
        if week and not month:
            # news_week url
            start = datetime.strptime(f"{datetime.now().year} {week} 1", "%Y %W %w")
            return InternetNews.objects.filter(timestamp__gte=start, timestamp__lte=start + timedelta(days=7))

        # news_day url
        if month and day:
            start = datetime.strptime(
                f"{datetime.now().year} {InternetNewsIndexView.url_month_mapping[month]} {day}", "%Y %m %d"
            )
            return InternetNews.objects.filter(timestamp__gte=start, timestamp__lte=start + timedelta(days=1))

        # news_month url
        if month:
            start = datetime.strptime(
                f"{datetime.now().year} {InternetNewsIndexView.url_month_mapping[month]} 01", "%Y %m %d"
            )
            return InternetNews.objects.filter(timestamp__gte=start, timestamp__lte=start.replace(month=start.month+1))

        # news_page url
        return InternetNews.objects.all()


    def get_queryset(self):
        queryset = self.get_time_filtered_queryset()

        # Random order queryset
        return queryset.order_by('?')


class InternetNewsRestViewSet(viewsets.ModelViewSet):
    """REST endpoints for basic CRUD operations on InternetNews"""
    queryset = InternetNews.objects.all()
    serializer_class = InternetNewsSerializer
    permission_classes = [permissions.IsAuthenticated]

class InternetLocationRestViewSet(viewsets.ModelViewSet):
    """REST endpoints for basic CRUD operations on InternetLocation"""
    queryset = InternetLocation.objects.all()
    serializer_class = InternetLocationSerializer
    permission_classes = [permissions.IsAuthenticated]
