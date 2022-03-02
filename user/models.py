from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime


class HelloUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.birthday = datetime(1970, 1, 1)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class HelloUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    email = models.EmailField(max_length=100, default='', verbose_name='邮箱')
    phone = models.CharField(max_length=50, default='', verbose_name='电话', null=True)
    nickname = models.CharField(max_length=20, verbose_name='昵称', default='匿名用户')
    avatar = models.URLField(verbose_name='头像',
                             default='http://cdn.hellofamily.club/'
                                     'logo%E7%9A%84%E5%89%AF%E6%9C%AC_Za0oX70.png')
    confirmed = models.BooleanField(default=False, verbose_name='验证用户')
    last_login = models.DateTimeField(null=True, verbose_name='上次登录时间')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    birthday = models.DateField(default='1970-01-01', verbose_name='生日')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = HelloUserManager()

    @property
    def is_staff(self):
        """
        判断用户是否为管理人员
        :return: True or False
        """
        return self.is_admin
