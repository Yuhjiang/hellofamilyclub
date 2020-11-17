from typing import Dict

from django.utils import timezone
from rest_framework import serializers
from django.core.validators import RegexValidator

from user.models import HelloUser
from utils.core.exceptions import HelloFamilyException
from utils.core.serializers import BasicSerializer

username_validator = RegexValidator(regex=r'^[a-zA-Z][a-zA-Z0-9_]*$',
                                    message='用户名只能包含大小写字母数字及下划线，必须以字母开头，最长32位')

special_characters = r'`~\!@#\$%\^&\*\(\)\-_\=\+\[\]\{\}\\\|\;:\'",./\?\<>'
password_validator = RegexValidator(
    regex=r'^(?![0-9]+$)(?![a-z]+$)(?![A-Z]+$)(?![{0}]+$)'
          r'[{0}0-9A-Za-z]{{8,16}}$'.format(special_characters),
    message='密码由大小写英文字母/数字/符号至少2种组成，8-16位字符'
)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    phone = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = HelloUser
        fields = ('id', 'username', 'nickname', 'email', 'phone', 'avatar',
                  'birthday', 'is_admin')


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[username_validator])
    password = serializers.CharField(validators=[password_validator])

    class Meta:
        model = HelloUser
        fields = ('username', 'password', 'nickname', 'email')

    def to_representation(self, instance: HelloUser):
        data = {
            'id': instance.id,
            'username': instance.username,
            'nickname': instance.nickname,
            'email': instance.email,
        }
        return data

    def create(self, validated_data: Dict):
        username = validated_data['username']
        password = validated_data['password']

        user = HelloUser.objects.create_user(username=username,
                                             password=password)
        user.email = validated_data['email']
        user.nickname = user.nickname
        user.save()

        return user


class LoginSerializer(BasicSerializer):
    username = serializers.CharField(label='用户名')
    password = serializers.CharField(label='密码')

    def validate(self, attrs: Dict):
        try:
            user = HelloUser.objects.get(username=attrs['username'])
            if user.is_active:
                return attrs
        except HelloUser.DoesNotExist:
            raise HelloFamilyException(
                HelloFamilyException.USERNAME_NOT_EXIST)
        else:
            raise HelloFamilyException(
                HelloFamilyException.USER_HAS_BEEN_BANNED)


class LoginResponseSerializer(BasicSerializer):
    isAdmin = serializers.BooleanField(label='是否是管理员')
    authToken = serializers.CharField(label='token')
    role = serializers.CharField(label='权限')
    id = serializers.IntegerField(label='用户id')
    avatar = serializers.CharField(label='用户头像')
    nickname = serializers.CharField(label='昵称')
    refreshToken = serializers.CharField(label='刷新token')
    login_time = serializers.DateTimeField(default=timezone.now)