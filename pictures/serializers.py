from rest_framework import serializers
import base64
from utils.core.serializers import BaseSerializer
from .models import Group, Member, CarouselPicture, MemberFace, Picture, PictureMember
from pictures.service import aip_service
from utils.core.exceptions import HelloFamilyError
import requests


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'name_jp', 'name_en', 'status', 'created_time',
                  'homepage', 'color',
                  'favicon', 'id']


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'name_jp')


class MemberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'name', 'name_jp')


class GroupSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name_jp', 'color']


class MemberSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name_jp', 'color']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        extra_kwargs = {
            'hometown': {'allow_blank': True},
            'nickname': {'allow_blank': True},
        }


class MemberWithGroupListSerializer(serializers.ModelSerializer):
    group_names = serializers.StringRelatedField(many=True, source='group')

    class Meta:
        model = Member
        fields = '__all__'


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


class MemberFaceCreateSerializer(BaseSerializer):
    url = serializers.URLField(label='图片url地址')
    member = serializers.IntegerField(label='成员id', write_only=True)
    face_id = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        url = validated_data['url']
        resp = requests.get(url)
        picture = resp.content
        picture = base64.b64encode(picture).decode('utf-8')
        member = Member.objects.get(id=validated_data['member'])
        face_id = aip_service.add_face(picture, member.name_en)
        if not face_id:
            raise HelloFamilyError(msg='人脸注册失败')
        return MemberFace.objects.create(member=member, face_id=face_id,
                                         url=url)


class MemberFaceSerializer(serializers.ModelSerializer):
    name_jp = serializers.CharField(source='member.name_jp')
    name_en = serializers.CharField(source='member.name_en')
    name = serializers.CharField(source='member.name')

    class Meta:
        model = MemberFace
        fields = ('id', 'member', 'face_id', 'create_time', 'name_jp',
                  'name_en', 'name')


class MemberInPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureMember
        fields = ('member_id', 'pic_id', 'name_en', 'name_jp')


class PictureWithMemberSerializer(serializers.ModelSerializer):
    members = MemberInPictureSerializer(source='picturemember_set', many=True)

    class Meta:
        model = Picture
        fields = ('id', 'pic_id', 'url', 'recognized', 'members')


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('id', 'pic_id', 'url', 'create_time', 'create_date')


class RecognizeSerializer(BaseSerializer):
    """
    人脸识别调用接口
    """
    id = serializers.IntegerField(label='图片id')