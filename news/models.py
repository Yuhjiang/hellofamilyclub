from django.db import models
from django.utils import timezone

from pictures.models import Group, Member


class NewsType(models.Model):
    name = models.CharField(max_length=20, verbose_name='资讯分类')
    color = models.CharField(max_length=20, verbose_name='主题色')
    is_nav = models.BooleanField(default=True, verbose_name='是否是导航')

    class Meta:
        verbose_name = verbose_name_plural = '资讯分类'

    def __str__(self):
        return self.name


class HelloNews(models.Model):
    """
    早安家族的动态，资讯
    """
    title = models.CharField(max_length=255, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    created_date = models.DateField(default=timezone.now, verbose_name='时间')
    source = models.URLField(verbose_name='原始链接')
    resource = models.TextField(null=True, verbose_name='资源')
    group = models.ManyToManyField(Group, verbose_name='相关组合')
    member = models.ManyToManyField(Member, verbose_name='相关成员')
    category = models.ForeignKey(NewsType, verbose_name='分类', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = verbose_name_plural = '资讯'
        ordering = ['-id']

    def __str__(self):
        return self.title + '-' + str(self.created_date)
