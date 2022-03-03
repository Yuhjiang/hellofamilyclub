import json

import requests
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet

from pictures import serializers
from pictures.filters import SinglePictureFilter, DoublePictureFilter
from pictures.models import Cookie, Group, Member, MemberFace, Picture
from utils.core.mixins import MultiActionConfViewSetMixin
from utils.core.permissions import AdminPermission


def get_weibo_response(cookie: str) -> requests.Response:
    resp = requests.get(settings.IMAGE_URL.format(1),
                        headers={'User-Agent': settings.USER_AGENT,
                                 'Cookie': cookie})
    return resp


class WeiboCookieView(GenericAPIView):
    """
    更新weibo爬虫的cookie
    """
    permission_classes = (AdminPermission,)
    serializer_class = serializers.CookieSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cookie_str = serializer.validated_data['cookie']
        resp = get_weibo_response(cookie_str)
        try:
            data = resp.json()
            if data['result']:
                c, _ = Cookie.objects.get_or_create(id=1)
                c.cookie = cookie_str
                c.save()
                return Response({'status': 200, 'errMsg': 'Cookie更新成功'})
            else:
                return Response({'status': 500, 'errMsg': 'Cookie更新失败'})
        except json.JSONDecodeError:
            return Response({'status': 500, 'errMsg': 'Cookie更新失败'})


class GroupViewSet(ModelViewSet):
    """
    团体的增删改查
    """
    serializer_class = serializers.GroupSerializer
    queryset = Group.objects.filter()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ('id',)
    search_fields = ('name', 'name_en', 'name_jp')
    filterset_fields = ('status',)


class GroupListView(mixins.ListModelMixin,
                    GenericViewSet):
    """
    获取所有的组合
    """
    serializer_class = serializers.GroupListSerializer
    pagination_class = None
    queryset = Group.objects.filter()


class MemberViewSet(MultiActionConfViewSetMixin,
                    ModelViewSet):
    """
    偶像的增删改查
    """
    serializer_class = serializers.MemberSerializer
    queryset = Member.objects.filter()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ('id',)
    search_fields = ('name', 'name_en', 'name_jp')
    filterset_fields = ('status', 'group')


class MemberListView(mixins.ListModelMixin,
                     GenericViewSet):
    """
    获取所有的成员
    """
    serializer_class = serializers.MemberListSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group',)
    queryset = Member.objects.filter().order_by('-status', 'joined_time')


class MemberFaceViewSet(MultiActionConfViewSetMixin,
                        ModelViewSet):
    """
    偶像人脸注册的增删改查
    """
    serializer_class = serializers.MemberFaceSerializer
    serializer_action_classes = {
        'create': serializers.MemberFaceCreateSerializer,
    }
    queryset = MemberFace.objects.filter()
    queryset_action_classes = {
        'list': queryset.select_related('member')
    }


class PictureMemberView(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    """
    获取照片和和对应的人脸
    """
    queryset = Picture.objects.filter().prefetch_related(
        'picturemember_set__member')
    serializer_class = serializers.PictureWithMemberSerializer


class PictureView(mixins.ListModelMixin,
                  GenericViewSet):
    """
    获取照片
    """
    queryset = Picture.objects.filter().order_by('-create_time')
    serializer_class = serializers.PictureSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SinglePictureFilter


class DoublePictureView(mixins.ListModelMixin,
                        GenericViewSet):
    """
    双成员CP查询
    """
    queryset = Picture.objects.filter(mem_count=2).order_by('-create_time')
    serializer_class = serializers.PictureSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DoublePictureFilter
