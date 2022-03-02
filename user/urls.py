from django.urls import path, include

from user import apis

urlpatterns = [
    path('/login', apis.login_user, name='login-user'),
    path('/register', apis.register_user, name='register-user'),
]