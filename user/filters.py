from django_filters import rest_framework as filters


from hellofamilyclub.utils.core.filters import BaseFilters
from user.models import HelloUser


class UserFilter(BaseFilters):
    username = filters.CharFilter(field_name='username', lookup_expr='contains')
    nickname = filters.CharFilter(field_name='nickname', lookup_expr='contains')
    email = filters.CharFilter(field_name='email', lookup_expr='email')

    class Meta:
        model = HelloUser
        fields = ['role', 'confirmed', 'is_admin']
