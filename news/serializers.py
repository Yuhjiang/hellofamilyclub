from rest_framework import serializers

from .models import NewsType, HelloNews
from pictures.serializers import GroupSerializerDetail, MemberSerializerDetail


class NewsTypeSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = NewsType
        fields = ['id', 'name', 'color']


class NewsTypeSerializerList(serializers.ModelSerializer):
    news_count = serializers.SerializerMethodField()

    class Meta:
        model = NewsType
        fields = ['id', 'name', 'color', 'is_nav', 'news_count']

    def get_news_count(self, obj):
        return obj.hellonews_set.count()


class NewsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsType
        fields = ['id', 'name', 'color', 'is_nav']


class HelloNewsSerializer(serializers.ModelSerializer):
    group = GroupSerializerDetail(many=True, read_only=True)
    member = MemberSerializerDetail(many=True, read_only=True)
    category = NewsTypeSerializerDetail(read_only=True)

    class Meta:
        model = HelloNews
        fields = ['id', 'title', 'content', 'created_date', 'resource', 'group', 'member',
                  'category']


class HelloNewsSerializerEdit(serializers.ModelSerializer):
    class Meta:
        model = HelloNews
        fields = ['id', 'title', 'content', 'created_date', 'resource', 'group', 'member',
                  'category']
