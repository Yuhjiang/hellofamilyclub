import json
from collections import defaultdict

import requests
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet

from pictures import serializers
from pictures.filters import SinglePictureFilter, DoublePictureFilter, \
    MemberFilter
from pictures.models import Cookie, Group, Member, MemberFace, Picture, \
    CarouselPicture
from pictures.service import WeiboCrawler, RecognizeService
from utils.cache import cache_client
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
                cache_client.delete(WeiboCrawler.ALERT_EMAIL_KEY)
                return Response({'status': 200, 'errMsg': 'Cookie更新成功'})
            else:
                return Response({'status': 500, 'errMsg': 'Cookie更新失败'})
        except json.JSONDecodeError:
            return Response({'status': 500, 'errMsg': 'Cookie更新失败'})


class GroupViewSet(MultiActionConfViewSetMixin,
                   ModelViewSet):
    """
    团体的增删改查
    """
    serializer_class = serializers.GroupSerializer
    queryset = Group.objects.filter()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ('id',)
    search_fields = ('name', 'name_en', 'name_jp')
    filterset_fields = ('status',)
    permission_classes = (AdminPermission,)
    permission_action_classes = {
        'list': (),
        'retrieve': (),
    }


class GroupListView(mixins.ListModelMixin,
                    GenericViewSet):
    """
    获取所有的组合
    """
    serializer_class = serializers.GroupListSerializer
    pagination_class = None
    queryset = Group.objects.filter().order_by('-status', 'created_time')


class MemberViewSet(MultiActionConfViewSetMixin,
                    ModelViewSet):
    """
    偶像的增删改查
    """
    serializer_class = serializers.MemberSerializer
    queryset = Member.objects.filter().order_by('-id')
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ('id',)
    search_fields = ('name', 'name_en', 'name_jp')
    filterset_class = MemberFilter
    permission_classes = (AdminPermission,)
    permission_action_classes = {
        'list': (),
        'retrieve': (),
    }
    serializer_action_classes = {
        'list': serializers.MemberWithGroupListSerializer,
    }


class MemberListView(mixins.ListModelMixin,
                     GenericViewSet):
    """
    获取所有的成员
    """
    serializer_class = serializers.MemberListSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group',)
    queryset = Member.objects.filter().order_by('-status', 'joined_time', 'id')


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


class GroupHistoryView(mixins.ListModelMixin,
                       GenericViewSet):
    """
    展示hello project所有的组合
    """
    queryset = Group.objects.filter().order_by('created_time')
    serializer_class = serializers.GroupSerializer
    pagination_class = None


class RecognizeView(GenericAPIView):
    """
    识别人脸的接口
    """
    serializer_class = serializers.RecognizeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pic = Picture.objects.get(id=serializer.validated_data['id'])
        service = RecognizeService([])
        members = service.recognize(pic)
        if members:
            pic.set_members(members)
            names = Member.objects.filter(id__in=members).values_list(
                'name', flat=True)
            return Response({'members': names, 'error': 200})
        else:
            return Response({'errMsg': '没有识别到成员', 'error': 500})


class MemberHistoryView(GenericAPIView):
    """
    成员的历史记录
    """
    queryset = Member.objects.filter().order_by('joined_time', '-status')
    serializer_class = serializers.MemberSerializer

    def get(self, request, *args, **kwargs):
        members = self.filter_queryset(self.get_queryset())
        member_dict = defaultdict(list)
        for m in members:
            data = self.get_serializer(m)
            member_dict[m.joined_time].append(data.data)
        member_list = []
        for k, v in member_dict.items():
            member_list.append({'joined_time': k, 'members': v})
        return Response(member_list)


class CarouselPictureView(mixins.ListModelMixin,
                          GenericViewSet):
    """
    首页的滚动图片
    """
    queryset = CarouselPicture.objects.filter(
        status=CarouselPicture.STATUS_NORMAL).order_by('-created_time')
    serializer_class = serializers.CarouselPictureSerializer
    pagination_class = None


def list_picture_to_date_group(data):
    date_group = defaultdict(list)
    for d in data:
        date_group[d['create_date']].append(d)
    return [{'create_date': k, 'pictures': v} for k, v in date_group.items()]


class TimelinePictureView(mixins.ListModelMixin,
                          GenericViewSet):
    """
    按照时间线展示用户
    """
    queryset = Picture.objects.filter().order_by('-create_time')
    serializer_class = serializers.PictureSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SinglePictureFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = list_picture_to_date_group(serializer.data)
        return Response({
            'count': self.paginator.page.paginator.count,
            'results': data,
        })


class TimelineDoublePictureView(mixins.ListModelMixin,
                                GenericViewSet):
    """
    双成员CP查询
    """
    queryset = Picture.objects.filter(mem_count=2).order_by('-create_time')
    serializer_class = serializers.PictureSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DoublePictureFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = list_picture_to_date_group(serializer.data)
        return Response({
            'count': self.paginator.page.paginator.count,
            'results': data,
        })
