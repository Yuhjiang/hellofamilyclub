import base64
import json
import zipfile
from datetime import datetime
from io import BytesIO

from aip import AipFace
from django.conf import settings
from django.db.models import Q
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework.permissions import IsAdminUser

from utils.decorators import admin_required_api
from utils.decorators import admin_required_api_normal
from utils.utils import download_picture, page_limit_skip
from utils.core.exceptions import HelloFamilyException
from pictures.tasks import recognize_picture
from .models import Group, Member, CarouselPicture
from .pagination import ListPagination
from .serializers import GroupSerializer, MemberSerializer, \
    CarouselPictureSerializer, \
    MemberCreateSerializer
from .service.config import mongo_db

APP_ID = settings.APP_ID
API_KEY = settings.API_KEY
SECRET_KEY = settings.SECRET_KEY
client = AipFace(APP_ID, API_KEY, SECRET_KEY)


class CookieAPI(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request):
        body = json.loads(request.body)
        if body.get('cookie'):
            current_time = datetime.now()
            result = mongo_db['cookie'].insert_one({
                'cookie': body['cookie'],
                'update_time': current_time,
            })
            if result.acknowledged:
                return Response({'errMsg': '',
                                 'data': {'message': '成功更新Cookie'}})
        raise HelloFamilyException(HelloFamilyException.COOKIE_UPDATE_ERROR)


class MemberFaceList(APIView):
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

    def get(self, request):
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit')
        if request.GET.get("group_second"):
            if request.GET.get('member_second') and int(
                    request.GET['member_second']):
                query = self.double_member(request.GET)
            else:
                try:
                    group = Group.objects.get(
                        id=int(request.GET["group_second"]))
                    query = {"members.group": group.name_en}
                except Group.DoesNotExist:
                    query = {}
        elif request.GET.get("group_first"):
            if request.GET.get('member_first') and int(
                    request.GET['member_first']):
                query = self.single_member(request.GET)
            else:
                try:
                    group = Group.objects.get(
                        id=int(request.GET["group_first"]))
                    query = {"members.group": group.name_en}
                except Group.DoesNotExist:
                    query = {}
        else:
            query = self.all_member()
        limit, skip = page_limit_skip(page, limit)
        images = list(mongo_db['images'].find(query, {'_id': 0}).
                      sort('created_time', -1).limit(limit).skip(skip))

        count = mongo_db['images'].count(query)
        result = {
            'status': 200,
            'errMsg': '',
            'data': {
                'images': images,
                'current': int(page),
                'limit': limit,
                'count': count
            },
        }
        return Response(result)


class MemberFaceListDate(MemberFaceList):
    def get(self, request):
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        if request.GET.get("group_second"):
            if request.GET.get('member_second') and int(
                    request.GET['member_second']):
                query = self.double_member(request.GET)
            else:
                try:
                    group = Group.objects.get(
                        id=int(request.GET["group_second"]))
                    query = {"members.group": group.name_en}
                except Group.DoesNotExist:
                    query = {}
        elif request.GET.get("group_first"):
            if request.GET.get('member_first') and int(
                    request.GET['member_first']):
                query = self.single_member(request.GET)
            else:
                try:
                    group = Group.objects.get(
                        id=int(request.GET["group_first"]))
                    query = {"members.group": group.name_en}
                except Group.DoesNotExist:
                    query = {}
        else:
            query = self.all_member()
        limit, skip = page_limit_skip(page, limit)
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
            "data": {
                'images': images,
                'count': count,
                'limit': limit,
                'page': page
            },
            "status": 200,
        }
        return Response(result)


class MemberFaceAPI(APIView):
    groupId = 'Hello_Project'

    @method_decorator(admin_required_api_normal)
    def post(self, request):
        """
        注册人脸
        :param request:
        :return:
        """
        body = request.POST
        try:
            member = Member.objects.get(id=body.get('member'))
        except Member.DoesNotExist:
            return Response({'status': '500', 'errMsg': '未找到成员'})
        user_id = member.name_en
        if body.get('image_url'):
            image = body['image_url']
            image_type = 'URL'
        else:
            # 前端传输文件，经过base64编码后向百度云注册
            file = request.FILES['files[]'].read()
            image = base64.b64encode(file).decode('utf-8')
            image_type = 'BASE64'
        result = client.addUser(image=image, image_type=image_type,
                                group_id=self.groupId, user_id=user_id)

        return Response({'status': '200', 'errMsg': result['error_msg']})

    def get(self, request):
        """
        获取人脸
        :param request:
        :return:
        """
        query = request.GET
        try:
            member = Member.objects.get(id=query.get('member'))
        except Member.DoesNotExist:
            return Response({'status': '500', 'errMsg': '未找到成员'})
        user_id = member.name_en

        faces = client.faceGetlist(user_id=user_id, group_id=self.groupId)

        return Response({'status': '200', 'data': {'faces': faces}})


class CarouselPictureViewSet(viewsets.ModelViewSet):
    serializer_class = CarouselPictureSerializer
    queryset = CarouselPicture.objects.filter()
    pagination_class = ListPagination

    @admin_required_api(message='你没有权限添加图片')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @admin_required_api(message='你没有权限修改图片')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @admin_required_api(message='你没有权限删除图片')
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = CarouselPicture.STATUS_DELETE
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    pagination_class = ListPagination

    def get_queryset(self):
        query_params = self.request.query_params
        params = {}

        if query_params.get('name_jp'):
            params['name_jp__contains'] = query_params['name_jp']
        if query_params.get('name_en'):
            params['name_en__contains'] = query_params['name_en']
        if query_params.get('start_date'):
            params['created_time__range'] = (
                datetime.strptime(query_params['start_date'],
                                  '%Y-%m-%d %H:%M:%S'),
                datetime.strptime(query_params['end_date'],
                                  '%Y-%m-%d %H:%M:%S'))

        new_queryset = self.queryset.filter(**params)

        if query_params.get('order'):
            new_queryset = new_queryset.order_by(query_params['order'])

        return new_queryset

    @admin_required_api(message='你没有权限添加组合')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @admin_required_api(message='你没有权限修改组合信息')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @admin_required_api(message='你没有权限删除组合')
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


class RecognizePicture(APIView):
    """
    主动请求识别人脸
    """
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        picture_name = request.data.get('pictureName')
        current_user = self.request.user

        recognize_picture.delay(current_user.id, picture_name)

        return Response({'data': 'success'}, status=status.HTTP_200_OK)


class DownloadPictures(APIView):
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        picture_list = request.data.get('picture_list')
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
