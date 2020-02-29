import json

from django.contrib import auth

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# from .models import HelloUser


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
                             'is_admin': user.is_admin,
                             'authToken': 'Bearer ' + str(token.access_token),
                             'role': user.role.permission,
                             'id': user.id,
                             'refresh': str(token),
                         }})
    else:
        return Response({'status': 500, 'errMsg': '用户名或密码错误'})
