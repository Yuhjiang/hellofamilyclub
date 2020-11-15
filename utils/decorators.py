from functools import wraps

from django.shortcuts import redirect
from rest_framework.response import Response

from user.models import HelloUser


def admin_required(function, redirect_url='/'):
    @wraps(function)
    def wrapped_function(request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return redirect(redirect_url)
    return wrapped_function


def admin_required_api_normal(function, message='你没有权限进行此操作'):
    @wraps(function)
    def wrapped_function(request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return Response({'status': 500, 'errMsg': message})
    return wrapped_function


def login_required(function, message='你没有权限进行此操作'):
    @wraps(function)
    def wrapped_function(request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return Response({'status': 302, 'errMsg': message, 'data': {
                'url': '/login',
            }})
    return wrapped_function


def login_required_api(message='你没有权限进行此操作'):
    def decorator(function):
        @wraps(function)
        def wrapped_function(self, request, *args, **kwargs):
            current_user = request.user
            if current_user.is_authenticated:
                return function(self, request, *args, **kwargs)
            else:
                return Response({'status': 302, 'errMsg': message, 'data': {
                    'url': '/login',
                }})
        return wrapped_function
    return decorator


def admin_required_api(message='你没有权限进行此操作'):
    def decorator(function):
        @wraps(function)
        def wrapped_function(self, request, *args, **kwargs):
            current_user = request.user
            if current_user.is_authenticated and current_user.is_staff:
                return function(self, request, *args, **kwargs)
            else:
                return Response({'status': 500, 'errMsg': message})
        return wrapped_function
    return decorator


def same_user_required_api(message='你没有权限进行此操作'):
    """
    管理员权限不受此装饰器限制
    """
    def decorator(function):
        @wraps(function)
        def wrapped_function(self, request, *args, **kwargs):
            current_user = request.user
            instance = self.get_object()
            if is_staff(current_user) or is_same_user(instance, current_user):
                return function(self, request, *args, **kwargs)
            else:
                return Response({'status': 500, 'errMsg': message})
        return wrapped_function
    return decorator


def is_same_owner(instance, current_user):
    return instance.owner_id == current_user.id


def is_staff(current_user):
    return current_user.is_staff


def is_same_user(instance, current_user):
    if isinstance(instance, HelloUser):
        return instance.id == current_user.id
    else:
        return is_same_owner(instance, current_user)