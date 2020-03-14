from rest_framework import serializers

from .models import Group, Member, CarouselPicture


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'name_jp', 'name_en', 'status', 'created_time', 'homepage', 'color',
                  'favicon', 'id']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['name_jp', 'name_en', 'name', 'status', 'joined_time',
                  'graduated_time', 'color', 'birthday', 'group_id', 'id']


class CarouselPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselPicture
        fields = ['id', 'name', 'image', 'status', 'created_time']