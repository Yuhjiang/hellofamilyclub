from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True
        else:
            return False
