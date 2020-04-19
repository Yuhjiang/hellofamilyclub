from django.db import models

from user.models import HelloUser as User


class Album(models.Model):
    owner = models.ForeignKey(User, verbose_name='创建者', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='相册名', default='默认相册')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(verbose_name='更新时间')

    def __str__(self):
        return '<{}>: <{}>'.format(self.owner.username, self.name)


class Picture(models.Model):
    owner = models.ForeignKey(User, verbose_name='上传者', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, verbose_name='图片名')
    description = models.CharField(max_length=255, null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    content = models.ImageField(verbose_name='图片')
    album = models.ForeignKey(Album, verbose_name='相册', on_delete=models.SET_NULL, blank=True,
                              null=True)
