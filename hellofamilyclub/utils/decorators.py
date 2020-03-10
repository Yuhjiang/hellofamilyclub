from functools import wraps

from django.shortcuts import redirect
from rest_framework.response import Response


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
        print(type(args[0]))
        current_user = request.user
        if current_user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return Response({'status': 302, 'errMsg': message, 'data': {
                'url': '/login',
            }})
    return wrapped_function


def login_required_api(function, message='你没有权限进行此操作'):
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


def admin_required_api(function, message='你没有权限进行此操作'):
    @wraps(function)
    def wrapped_function(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user.is_staff:
            return function(self, request, *args, **kwargs)
        else:
            return Response({'status': 500, 'errMsg': message})
    return wrapped_function
