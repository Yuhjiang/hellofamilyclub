from rest_framework import routers
from django.urls import path, include

from user import views

router = routers.SimpleRouter()

router.register('', views.UserViewSet, basename='user')

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='user-register'),
    path('login/', views.LoginUser.as_view(), name='user-login'),
    path('', include(router.urls))
]