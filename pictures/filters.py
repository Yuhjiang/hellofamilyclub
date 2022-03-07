from django_filters import rest_framework as filters

from pictures.models import Picture, Member


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


class MemberFilter(filters.FilterSet):
    group_names = filters.CharFilter(field_name='group__name', lookup_expr='icontains')
    name_jp = filters.CharFilter(field_name='name_jp', lookup_expr='icontains')
    name_en = filters.CharFilter(field_name='name_en', lookup_expr='icontains')
    start_date = filters.DateFilter(field_name='joined_time', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='joined_time', lookup_expr='lte')

    class Meta:
        model = Member
        fields = ('group_names', 'group', 'name_jp', 'name_en', 'status',
                  'start_date', 'end_date')
