from django_filters import rest_framework as filters

from pictures.models import Picture


class SinglePictureFilter(filters.FilterSet):
    """
    单成员图片搜索
    """
    group = filters.NumberFilter(field_name='picturemember__member__group')
    member = filters.NumberFilter(field_name='picturemember__member')

    class Meta:
        model = Picture
        fields = ('group', 'member')


class DoublePictureFilter(filters.FilterSet):
    """
    成员CP搜索
    """
    double = filters.CharFilter(field_name='double')

    class Meta:
        model = Picture
        fields = ('double',)
