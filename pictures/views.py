import base64
import zipfile
from datetime import datetime
from io import BytesIO

from aip import AipFace
from django.conf import settings
from django.db.models import Q
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pictures.filters import CarouselFilter, GroupFilter
from pictures.models import Group, Member, CarouselPicture
from pictures.pagination import ListPagination
from pictures.serializers import GroupSerializer, MemberSerializer, \
    CarouselPictureSerializer, MemberCreateSerializer, CookieSerializer, \
    MemberFaceSerializer, MemberFaceResultSerializer, FaceRegisterSerializer, \
    FaceRecognizeSerializer, DownloadPictureListSerializer,\
    MemberFaceListSerializer, MemberFaceFilterSerializer, MemberFaceDateSerializer
from pictures.service.config import mongo_db
from pictures.tasks import recognize_picture
from utils.core.exceptions import HelloFamilyException, ErrorCode
from utils.core.mixins import MultiActionConfViewSetMixin
from utils.decorators import admin_required_api
from utils.utils import download_picture, page_limit_skip

APP_ID = settings.APP_ID
API_KEY = settings.API_KEY
SECRET_KEY = settings.SECRET_KEY
client = AipFace(APP_ID, API_KEY, SECRET_KEY)


class CookieAPI(APIView):
    permission_classes = (IsAdminUser,)

    @method_decorator(swagger_auto_schema(
        request_body=CookieSerializer(),
        operation_summary='更新Cookie',
        responses={'200': 'No Content'}
    ))
    def post(self, request):
        serializer = CookieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        current_time = datetime.now()
        result = mongo_db['cookie'].insert_one({
            'cookie': data['cookie'],
            'update_time': current_time,
        })
        return Response(status=status.HTTP_200_OK)


class MemberFaceList(APIView):
    limit = 20
    
    @staticmethod
    def all_member():
        return {}

    @staticmethod
    def single_member(query):
        return {'members.id': int(query['member_first'])}

    @staticmethod
    def double_member(query):
        member_1 = int(query['member_first'])
        member_2 = int(query['member_second'])
        query = {'$or': [{'members.1.id': member_1, 'members.0.id': member_2},
                         {'members.1.id': member_2, 'members.0.id': member_1}],
                 'size': 2}
        return query

    @method_decorator(swagger_auto_schema(
        query_serializer=MemberFaceFilterSerializer(),
        operation_summary='表格显示的成员图片',
        responses={'200': openapi.Response('成员图片响应',
                                           MemberFaceListSerializer())}
    ))
    def get(self, request):
        serializer = MemberFaceFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        if data.get("group_second"):
            if data.get('member_second') and int(
                    data['member_second']):
                query = self.double_member(data)
            else:
                try:
                    group = Group.objects.get(
                        id=int(data["group_second"]))
                    query = {"members.group": group.name_en}
                except Group.DoesNotExist:
                    query = {}
        elif data.get("group_first"):
            if data.get('member_first') and int(
                    data['member_first']):
                query = self.single_member(data)
            else:
                try:
                    group = Group.objects.get(
                        id=int(data["group_first"]))
                    query = {"members.group": group.name_en}
                except Group.DoesNotExist:
                    query = {}
        else:
            query = self.all_member()

        limit, skip = page_limit_skip(data['page'], self.limit)
        images = list(mongo_db['images'].find(query, {'_id': 0}).
                      sort('created_time', -1).limit(limit).skip(skip))

        count = mongo_db['images'].count(query)
        result = {
            'count': count,
            'results': images,
        }
        return Response(result)


class MemberFaceListDate(MemberFaceList):
    @method_decorator(swagger_auto_schema(
        query_serializer=MemberFaceFilterSerializer(),
        operation_summary='表格显示的成员图片',
        responses={'200': openapi.Response('成员图片响应',
                                           MemberFaceDateSerializer())}
    ))
    def get(self, request):
        serializer = MemberFaceFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        if data.get("group_second"):
            if data.get('member_second') and int(
                    data['member_second']):
                query = self.double_member(data)
            else:
                try:
                    group = Group.objects.get(
                        id=int(data["group_second"]))
                    query = {"members.group": group.name_en}
                except Group.DoesNotExist:
                    query = {}
        elif data.get("group_first"):
            if data.get('member_first') and int(
                    data['member_first']):
                query = self.single_member(data)
            else:
                try:
                    group = Group.objects.get(
                        id=int(data["group_first"]))
                    query = {"members.group": group.name_en}
                except Group.DoesNotExist:
                    query = {}
        else:
            query = self.all_member()
        limit, skip = page_limit_skip(data['page'], self.limit)
        count = mongo_db['images'].count(query)
        images = list(mongo_db['images'].aggregate([
            {'$match': query},
            {'$sort': {'created_time': -1}},
            {'$skip': skip},
            {'$limit': limit},
            {'$group': {
                '_id': '$created_date',
                'pictures': {'$push': {'name': '$name', 'url': '$url'}},
                'date': {'$first': 1}
            }},
            {'$sort': {'_id': -1}},
        ]))
        for image in images:
            image['date'] = image['_id'].strftime('%Y年%m月%d日')
        result = {
            'count': count,
            'results': images,
        }
        return Response(result)


class MemberFaceAPI(APIView):
    groupId = 'Hello_Project'

    @method_decorator(swagger_auto_schema(
        operation_summary='注册人脸',
        request_body=FaceRegisterSerializer,
        responses={
            '200': 'No content',
            '499': 'error'
        }
    ))
    def post(self, request):
        data = request.data
        try:
            member = Member.objects.get(id=data['member'])
        except Member.DoesNotExist:
            raise HelloFamilyException(ErrorCode.MEMBER_NOT_EXISTS)

        file = request.FILES['image'].read()
        image = base64.b64encode(file).decode('utf-8')
        image_type = 'BASE64'

        result = client.addUser(image=image, image_type=image_type,
                                group_id=self.groupId, user_id=member.name_en)
        if result['error_msg'] == 'SUCCESS':
            return Response(status=status.HTTP_200_OK)
        raise HelloFamilyException(ErrorCode.FACE_REGISTER_FAIL)

    @method_decorator(swagger_auto_schema(
        query_serializer=MemberFaceSerializer(),
        operation_summary='获取百度人脸库里的信息',
        responses={'200': openapi.Response('人脸库返回的列表',
                                           MemberFaceResultSerializer())}
    ))
    def get(self, request):
        query = request.GET
        try:
            member = Member.objects.get(id=query.get('member'))
        except Member.DoesNotExist:
            raise HelloFamilyException(ErrorCode.MEMBER_NOT_EXISTS)
        user_id = member.name_en

        faces = client.faceGetlist(user_id=user_id, group_id=self.groupId)
        faces['user_id'] = user_id
        serializer = MemberFaceResultSerializer(data=faces)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        return Response(data)


class CarouselPictureViewSet(MultiActionConfViewSetMixin,
                             viewsets.ModelViewSet):
    serializer_class = CarouselPictureSerializer
    queryset = CarouselPicture.objects.filter()
    permission_classes = (IsAdminUser,)
    permission_action_classes = {
        'list': (permissions.AllowAny,),
    }
    filter_class = CarouselFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = CarouselPicture.STATUS_DELETE
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    pagination_class = ListPagination
    filter_class = GroupFilter
    ordering_fields = ['id', 'created_time']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Group.STATUS_DISBAND
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MemberViewSet(viewsets.ModelViewSet):
    # TODO 后续需要在添加或修改成员信息的时候，重新注册一下人脸
    serializer_class = MemberSerializer
    queryset = Member.objects.all().order_by('-status', 'joined_time')
    pagination_class = ListPagination

    def get_queryset(self):
        query_params = self.request.query_params

        params = {}
        param_args = []
        if query_params.get('group_id'):
            params['group_id'] = query_params['group_id']
        if query_params.get('group'):
            param_args.append(Q(group__name_en__contains=query_params['group'])
                              | Q(
                group__name_jp__contains=query_params['group']))
        if query_params.get('name_jp'):
            params['name_jp__contains'] = query_params['name_jp']
        if query_params.get('name_en'):
            params['name_en__contains'] = query_params['name_en']
        if query_params.get('start_date'):
            params['joined_time__range'] = (
                datetime.strptime(query_params['start_date'],
                                  '%Y-%m-%d %H:%M:%S'),
                datetime.strptime(query_params['end_date'],
                                  '%Y-%m-%d %H:%M:%S'))

        new_queryset = self.queryset.filter(*param_args, **params)
        return new_queryset

    @admin_required_api(message='你没有权限添加成员')
    def create(self, request, *args, **kwargs):
        self.serializer_class = MemberCreateSerializer
        return super().create(request, *args, **kwargs)

    @admin_required_api(message='你没有权限修改成员信息')
    def update(self, request, *args, **kwargs):
        self.serializer_class = MemberCreateSerializer
        return super().update(request, *args, **kwargs)

    @admin_required_api(message='你没有权限删除成员')
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Member.STATUS_GRADUATED
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RecognizePicture(GenericAPIView):
    """
    主动请求识别人脸
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FaceRecognizeSerializer

    @method_decorator(swagger_auto_schema(
        operation_summary='主动请求识别人脸',
        responses={'200': 'No Content'}
    ))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        picture_name = serializer.data['picture_name']
        current_user = self.request.user

        recognize_picture.delay(current_user.id, picture_name)

        return Response(status=status.HTTP_200_OK)


class DownloadPictures(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DownloadPictureListSerializer

    @method_decorator(swagger_auto_schema(
        operation_summary='下载当前页面的图片',
        responses={'200': '下载文件的二进制流'}
    ))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        picture_list = serializer.data['picture_list']

        zip_file = BytesIO()
        with zipfile.ZipFile(zip_file, 'a') as f:
            for picture in picture_list:
                pic = download_picture(picture['url'], save=False)
                f.writestr(picture['name'], BytesIO(pic).getvalue())

        zip_file.seek(0)
        response = HttpResponse(zip_file.getvalue(),
                                content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=图片.zip'
        return response
