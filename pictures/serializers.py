from typing import Dict
import requests
import json

from django.conf import settings
from rest_framework import serializers

from pictures.models import Group, Member, CarouselPicture, Face
from utils.core.serializers import BasicSerializer
from utils.core.exceptions import HelloFamilyException


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'name_jp', 'name_en', 'status', 'created_time', 'homepage', 'color',
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
    status = serializers.ChoiceField(
        choices=CarouselPicture.STATUS_ITEMS,
        help_text=(str(CarouselPicture.STATUS_ITEMS)),
        required=False,
    )

    class Meta:
        model = CarouselPicture
        fields = ['id', 'name', 'image', 'status', 'created_time']


class CookieSerializer(BasicSerializer):
    cookie = serializers.CharField(label='微博Cookie')

    def validate(self, attrs: Dict) -> Dict:
        try:
            url = settings.IMAGE_URL.format('1')
            headers = {
                'User-Agent': settings.USER_AGENT,
                'Cookie': attrs['cookie']}
            requests.get(url, headers=headers).json()
        except json.decoder.JSONDecodeError:
            raise HelloFamilyException(HelloFamilyException.COOKIE_UPDATE_ERROR)
        return attrs


class MemberFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id']


class FaceSerializer(BasicSerializer):
    face_token = serializers.CharField(label='人脸唯一标示，可以通过token获取到人脸照片')
    ctime = serializers.DateTimeField(label='注册时间', format='%Y-%m-%d %H:%M:%S')
    face_url = serializers.CharField(label='人脸照片URL')


class MemberFaceResultSerializer(BasicSerializer):
    face_list = serializers.ListField(child=FaceSerializer())

    def to_internal_value(self, data: Dict) -> Dict:
        """
        {
            "error_code": 0,
            "error_msg": "SUCCESS",
            "log_id": 2012010014584,
            "timestamp": 1605624516,
            "cached": 0,
            "result": {
                "face_list": [
                    {
                        "face_token": "d47b79cc9bbf098e85b0af00c9ce6489",
                        "ctime": "2019-07-19 11:44:49"
                    },
                    {
                        "face_token": "4b7d684f626c03f2c0de1d3f88c1d426",
                        "ctime": "2019-07-19 11:40:15"
                    },
                    {
                        "face_token": "5ace50b26d04af5759bbe67aeec8bf50",
                        "ctime": "2020-02-15 16:03:12"
                    },
                    {
                        "face_token": "1c3cac40d75171111ebd278f5dd3b9b6",
                        "ctime": "2020-03-06 21:37:48"
                    }
                ]
            }
        :param data:
        :return:
        """
        result = data['result']
        face_list = result['face_list']
        for i in range(len(face_list)):
            d = dict(
                face_token=face_list[i]['face_token'],
                ctime=face_list[i]['ctime'],
                user_id=data['user_id']
            )
            face_list[i] = Face(**d)

        return result


class FaceRegisterSerializer(BasicSerializer):
    image = serializers.CharField(label='图片，需要放进formdata里')
    member = serializers.IntegerField(label='成员id')

