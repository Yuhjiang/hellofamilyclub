from django.db import models

from user.models import HelloUser as User
from album.models import Album


class Category(models.Model):
    """
    博客分类
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称', unique=True)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS,
                                         verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='创建者', on_delete=models.DO_NOTHING)
    color = models.CharField(max_length=20, verbose_name='颜色', null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name='名称', unique=True)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS,
                                         verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='创建者', on_delete=models.DO_NOTHING)
    color = models.CharField(max_length=20, verbose_name='颜色', null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, verbose_name='摘要')
    content = models.TextField(verbose_name='正文')
    draft = models.TextField(verbose_name='草稿', blank=True)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS,
                                         verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(null=True, verbose_name='更新时间')
    is_md = models.BooleanField(default=False, verbose_name='markdown语法')
    amount = models.PositiveIntegerField(default=1, verbose_name='阅读量')

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )

    content = models.TextField(verbose_name='评论')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING,
                              related_name='owner')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    post = models.ForeignKey(Post, verbose_name='文章', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, verbose_name='被评论者', on_delete=models.DO_NOTHING,
                                related_name='to_user')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, verbose_name='状态',
                                         choices=STATUS_ITEMS)

    def __str__(self):
        return self.content
