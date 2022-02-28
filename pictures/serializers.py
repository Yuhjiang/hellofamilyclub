from rest_framework import serializers

from utils.core.serializers import BaseSerializer
from .models import Group, Member, CarouselPicture


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'name_jp', 'name_en', 'status', 'created_time',
                  'homepage', 'color',
                  'favicon', 'id']


class GroupSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name_jp', 'color']


class MemberSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name_jp', 'color']


class MemberSerializer(serializers.ModelSerializer):
    group = GroupSerializerDetail()

    class Meta:
        model = Member
        fields = ['name_jp', 'name_en', 'name', 'status', 'joined_time',
                  'graduated_time', 'color', 'birthday', 'group', 'id']


class MemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['name_jp', 'name_en', 'name', 'status', 'joined_time',
                  'graduated_time', 'color', 'birthday', 'group', 'id']


class CarouselPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselPicture
        fields = ['id', 'name', 'image', 'status', 'created_time']


class CookieSerializer(BaseSerializer):
    cookie = serializers.CharField(label='更新cookie')
