from rest_framework import routers
from django.urls import path

from user import views

router = routers.SimpleRouter()

router.register('/', views.UserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns.extend(
    [
        path('register/', views.RegisterUser.as_view(), name='user-register'),
        path('login/', views.LoginUser.as_view(), name='user-login'),
    ]
)