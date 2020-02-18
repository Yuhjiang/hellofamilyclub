from rest_framework import serializers

from .models import Group, Member


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name_jp', 'status', 'created_time', 'homepage', 'color',
                  'favicon', 'id']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['name_jp', 'name_en', 'name', 'status', 'joined_time',
                  'graduated_time', 'color', 'birthday', 'group_id', 'id']
