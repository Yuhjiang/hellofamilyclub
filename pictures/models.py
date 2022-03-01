"""
早安家族人脸识别模块，调用百度aip
"""
from django.db import models


class Group(models.Model):
    STATUS_NORMAL = 1
    STATUS_DISBAND = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DISBAND, '解散')
    )

    name = models.CharField(max_length=50, verbose_name='组合名')
    name_jp = models.CharField(max_length=50, verbose_name='日文')
    name_en = models.CharField(max_length=50, verbose_name='罗马')
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateField(null=True, verbose_name='成立时间')
    homepage = models.URLField(null=True, verbose_name='主页')
    color = models.CharField(max_length=20, verbose_name='颜色')
    favicon = models.URLField(verbose_name='照片')

    class Meta:
        verbose_name = verbose_name_plural = '组合'

    def __str__(self):
        return self.name_jp

    @classmethod
    def get_all(cls, status=None):
        if not status:
            return cls.objects.all()
        else:
            return cls.objects.filter(status=Group.STATUS_NORMAL)

    def get_all_members(self):
        return self.member_set.all()

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.filter(name__contains=name)


class Member(models.Model):
    STATUS_NORMAL = 1
    STATUS_GRADUATED = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '在籍'),
        (STATUS_GRADUATED, '毕业')
    )

    name = models.CharField(max_length=50, verbose_name='成员')
    name_jp = models.CharField(max_length=50, verbose_name='日文')
    name_en = models.CharField(max_length=50, verbose_name='罗马')
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    joined_time = models.DateField(verbose_name='进入时间', null=True, blank=True)
    graduated_time = models.DateField(null=True, verbose_name='毕业时间')
    group = models.ManyToManyField(Group, verbose_name='组合')
    favicon = models.URLField(null=True, verbose_name='照片')
    color = models.CharField(null=True, max_length=20, verbose_name='成员色')
    birthday = models.DateField(null=True, verbose_name='生日', blank=True)
    hometown = models.CharField(max_length=50, verbose_name='出生地')
    nickname = models.CharField(max_length=50, verbose_name='昵称')

    class Meta:
        verbose_name = verbose_name_plural = '成员'
        ordering = ['-id']

    def __str__(self):
        return self.name

    @classmethod
    def get_all(cls, status=None):
        if not status:
            return cls.objects.all()
        else:
            return cls.objects.filter(status=Group.STATUS_NORMAL)

    @classmethod
    def get_by_group(cls, group_id, status=None):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            members = []
        else:
            if not status:
                members = group.member_set.all()
            else:
                members = group.member_set.filter(status=Member.STATUS_NORMAL)

        return members.select_related('group')


class MemberFace(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, help_text='头像地址')
    create_time = models.DateTimeField(auto_now_add=True)
    face_id = models.CharField(verbose_name='人脸识别的id', max_length=255)

    class Meta:
        ordering = ('-id',)


class CarouselPicture(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=120, verbose_name='名称')
    image = models.URLField(verbose_name='图片')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @property
    def current_images(self):
        return self.objects.filter(status=self.STATUS_NORMAL)


class Cookie(models.Model):
    cookie = models.TextField(verbose_name='cookie')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '爬虫Cookie'


class Picture(models.Model):
    pic_id = models.CharField(verbose_name='id', unique=True, max_length=100)
    name = models.CharField(verbose_name='图片名字', max_length=255)
    url = models.CharField(verbose_name='链接地址', max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    create_date = models.DateField(auto_now_add=True)
    mem_count = models.IntegerField(verbose_name='图片里的人数')
    download = models.BooleanField(default=False, verbose_name='是否已下载')
    recognized = models.BooleanField(default=False, verbose_name='是否被识别过')

    class Meta:
        verbose_name = '下载的图片'

    def __str__(self):
        return f'pic_id: {self.pic_id}, name: {self.name}, url: {self.url}, ' \
               f'mem_count: {self.mem_count}, download: {self.download}, ' \
               f'recognized: {self.recognized}'


class PictureMember(models.Model):
    pic = models.ForeignKey(Picture, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '图片和成员的关联关系'
