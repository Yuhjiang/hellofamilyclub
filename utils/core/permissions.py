from rest_framework.permissions import BasePermission

from user.models import HelloUser
from utils.core import HelloFamilyException


def is_same_user(instance, current_user):
    if isinstance(instance, HelloUser):
        return instance.id == current_user.id
    else:
        return is_same_owner(instance, current_user)


def is_same_owner(instance, current_user):
    return instance.owner_id == current_user.id


class SameUserPermission(BasePermission):
    """
    用户和操作的数据必须是同一个人
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT']:
            if (request.user and request.user.is_statff) or \
                    is_same_user(obj, request.user):
                return True
            raise HelloFamilyException(HelloFamilyException.SAME_USER_REQUIRED)
        return True
