from datetime import datetime

from django.contrib import auth
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework_simplejwt.tokens import RefreshToken

from user.filters import UserFilter
from user.models import HelloUser
from user.serializers import UserSerializer, RegisterSerializer, \
    LoginSerializer, LoginResponseSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = UserSerializer
    queryset = HelloUser.objects.filter()
    permission_classes = (IsAdminUser, )
    filterset_class = UserFilter


class RegisterUser(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUser(GenericAPIView):
    serializer_class = LoginSerializer

    @method_decorator(swagger_auto_schema(
        operation_description='登录接口',
        responses={'200': LoginResponseSerializer()}
    ))
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        user = auth.authenticate(username=data['username'],
                                 password=data['password'])
        token = RefreshToken.for_user(user)
        return Response({
            'isAdmin': user.is_admin,
            'authToken': str(token.access_token),
            'role': user.role.permission,
            'id': user.id,
            'avatar': user.avatar,
            'nickname': user.nickname,
            'refreshToken': str(token),
            'login_time': datetime.now()
        }, status=status.HTTP_200_OK)
