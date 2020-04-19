import json
from datetime import datetime

from django.contrib import auth

from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import HelloUser
from .serializers import UserSerializer
from .pagination import ListPagination
from album.models import Album
from hellofamilyclub.utils.decorators import admin_required_api, same_user_required_api


@api_view(['POST'])
def login_user(request):
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    user = auth.authenticate(username=username, password=password)
    if user and user.is_active:
        token = RefreshToken.for_user(user)
        return Response({'status': 200, 'errMsg': '',
                         'data': {
                             'isAdmin': user.is_admin,
                             'authToken': str(token.access_token),
                             'role': user.role.permission,
                             'id': user.id,
                             'avatar': user.avatar,
                             'nickname': user.nickname,
                             'refreshToken': str(token),
                         }})
    else:
        return Response({'status': 500, 'errMsg': '用户名或密码错误'})


@api_view(['POST'])
def register_user(request):
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    nickname = body.get('nickname')
    email = body.get('email')

    username = HelloUser.normalize_username(username)
    user = HelloUser(username=username, nickname=nickname, email=email)
    user.set_password(password)
    user.save()
    # 创建默认相册
    album = Album(owner_id=user.id, updated_time=datetime.now())
    album.save()

    return Response({'status': 200, 'errMsg': '',
                     'data': {
                         'id': user.id,
                         'username': user.username,
                         'nickname': user.nickname,
                         'isAdmin': user.is_admin,
                     }})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = HelloUser.objects.filter()
    pagination_class = ListPagination

    def get_queryset(self):
        query_params = self.request.query_params
        params = {}

        if query_params.get('username'):
            params['username__contains'] = query_params['username']
        if query_params.get('nickname'):
            params['nickname__contains'] = query_params['nickname']
        if query_params.get('email'):
            params['email__contains'] = query_params['email']

        new_queryset = self.queryset.filter(**params)
        return new_queryset

    @admin_required_api
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @same_user_required_api(message='你没有权限修改用户信息')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @admin_required_api
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
