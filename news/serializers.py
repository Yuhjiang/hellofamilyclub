from rest_framework import serializers

from .models import NewsType, HelloNews


class NewsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsType
        fields = ['name', 'color', 'is_nav']


class HelloNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelloNews
        fields = ['title', 'content', 'created_date', 'resource', 'group', 'member', 'type']
