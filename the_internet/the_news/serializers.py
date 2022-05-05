
from rest_framework import serializers

from .models import InternetLocation, InternetNews


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
