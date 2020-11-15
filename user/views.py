import json
from datetime import datetime

from django.contrib import auth

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import HelloUser
from user.serializers import UserSerializer
from album.models import Album
from user.filters import UserFilter
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
                             'login_time': datetime.now()
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
    permission_classes = [IsAdminUser, ]
    filterset_class = UserFilter

    @admin_required_api
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @same_user_required_api(message='你没有权限修改用户信息')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @admin_required_api
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
