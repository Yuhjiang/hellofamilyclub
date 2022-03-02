from datetime import datetime
from io import BytesIO
import zipfile

from django.db.models import Q
from django.http.response import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

from .models import Group, Member, CarouselPicture
from .serializers import GroupSerializer, MemberSerializer, CarouselPictureSerializer, \
    MemberCreateSerializer
from hellofamilyclub.utils.decorators import admin_required_api
from hellofamilyclub.utils.utils import download_picture



class CarouselPictureViewSet(viewsets.ModelViewSet):
    serializer_class = CarouselPictureSerializer
    queryset = CarouselPicture.objects.filter()

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

    def get_queryset(self):
        query_params = self.request.query_params

        params = {}
        param_args = []
        if query_params.get('group_id'):
            params['group_id'] = query_params['group_id']
        if query_params.get('group'):
            param_args.append(Q(group__name_en__contains=query_params['group'])
                              | Q(group__name_jp__contains=query_params['group']))
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
    authentication_classes = (authentication.JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        picture_name = request.data.get('pictureName')
        current_user = self.request.user


        return Response({'data': 'success'}, status=status.HTTP_200_OK)


class DownloadPictures(APIView):
    authentication_classes = (authentication.JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

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
