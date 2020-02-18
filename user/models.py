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


class Role(models.Model):
    name = models.CharField(max_length=50, verbose_name='角色名')
    permission = models.PositiveIntegerField(default=1, verbose_name='权限等级')
    desc = models.CharField(max_length=100, verbose_name='权限描述')


class HelloUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    email = models.EmailField(max_length=100, default='', verbose_name='邮箱')
    phone = models.CharField(max_length=50, default='', verbose_name='电话')
    role = models.ForeignKey(Role, verbose_name='角色', default=2,
                             on_delete=models.DO_NOTHING)
    confirmed = models.BooleanField(default=False, verbose_name='验证用户')
    last_login = models.DateTimeField(null=True, verbose_name='上次登录时间')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    birthday = models.DateTimeField(null=True, verbose_name='生日')
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

    @property
    def is_superuser(self):
        """
        管理员顶级权限
        :return: True or False
        """
        return self.role.permission == 99
