from datetime import datetime

from rest_framework import serializers

from .models import Album, Picture
from user.models import HelloUser


class AlbumSerializer(serializers.ModelSerializer):
    picture_count = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ('id', 'name', 'created_time', 'owner', 'updated_time', 'picture_count')

    @staticmethod
    def get_picture_count(obj):
        return obj.picture_set.count()

    def create(self, validated_data):
        album = Album(**validated_data)
        album.updated_time = datetime.now()
        album.save()
        return album

    def update(self, instance, validated_data):
        instance.updated_time = datetime.now()
        return super().update(instance, validated_data)


class PictureSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Picture
        fields = ('id', 'name', 'owner', 'created_time', 'content')
