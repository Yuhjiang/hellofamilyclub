from django_filters import rest_framework as filters

from utils.core.filters import BaseFilters
from pictures.models import CarouselPicture, Group


class CarouselFilter(BaseFilters):
    class Meta:
        model = CarouselPicture
        fields = ['status']


class GroupFilter(BaseFilters):
    name_jp = filters.CharFilter(field_name='name_jp', lookup_expr='contains')
    name_en = filters.CharFilter(field_name='name_en', lookup_expr='contains')
    start_date = filters.DateTimeFilter(field_name='created_time',
                                        lookup_expr='created_time__gt')
    end_date = filters.DateTimeFilter(field_name='created_time',
                                      lookup_expr='created_time__lt')

    class Meta:
        model = Group
        fields = ['name_jp', 'name_en', 'start_date', 'end_date', 'status']