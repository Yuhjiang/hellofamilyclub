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
    homepage = models.URLField(verbose_name='主页')
    color = models.CharField(max_length=20, verbose_name='颜色')
    favicon = models.URLField(verbose_name='照片')

    class Meta:
        verbose_name = verbose_name_plural = '组合'

    def __str__(self):
        return self.name

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
    joined_time = models.DateField(null=True, verbose_name='进入时间')
    graduated_time = models.DateField(null=True, verbose_name='毕业时间')
    group = models.ForeignKey(Group, verbose_name='组合',
                              on_delete=models.DO_NOTHING)
    favicon = models.URLField(verbose_name='照片')
    color = models.CharField(max_length=20, verbose_name='成员色')
    birthday = models.DateField(null=True, verbose_name='生日')
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
