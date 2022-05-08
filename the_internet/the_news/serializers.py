
from rest_framework import serializers

from the_news.models import InternetLocation, InternetNews


class InternetNewsListSerializer(serializers.ListSerializer):
    """Default list serialiser for InternetNews """

class InternetNewsSerializer(serializers.HyperlinkedModelSerializer):
    """InternetNews serializer default model"""

    class Meta:
        """Meta data for InternetNewsSerializer"""
        model = InternetNews
        list_serializer_class = InternetNewsListSerializer
        fields = '__all__'

class InternetLocationSerializer(serializers.HyperlinkedModelSerializer):
    """InternetLocation serializer default model"""

    class Meta:
        """Meta data for InternetLocationSerializer"""
        model = InternetLocation
        fields = '__all__'
