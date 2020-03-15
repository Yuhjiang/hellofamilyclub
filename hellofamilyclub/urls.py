"""hellofamilyclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from pictures.views import MemberFaceAPI, MemberFace, MemberFaceIndex, \
    MemberFaceList, GroupProfile, MemberFaceListDate, CookieAPI
from pictures.apis import CarouselPictureViewSet, GroupViewSet, MemberViewSet
from pictures.autocomplete import MemberAutoComplete
from user.apis import login_user, register_user, UserViewSet
from blog.apis import PostViewSet, CategoryViewSet, TagViewSet, upload_picture, CommentViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='api-post')
router.register(r'category', CategoryViewSet, basename='api-category')
router.register(r'tag', TagViewSet, basename='api-tag')
router.register(r'user', UserViewSet, basename='api-user')
router.register(r'carousel', CarouselPictureViewSet, basename='api-carousel')
router.register(r'group', GroupViewSet, basename='api-group')
router.register(r'member', MemberViewSet, basename='api-member')
router.register(r'comment', CommentViewSet, basename='api-comment')

urlpatterns = [
    path('api/upload_picture', upload_picture, name='upload-picture'),
    path('api/', include(router.urls)),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/login', login_user, name='login-user'),
    path('api/register', register_user, name='register-user'),
    path('api/cookie', CookieAPI.as_view(), name='cookie'),
    path('api/pictures/timeline/', MemberFaceListDate.as_view(),
         name='faces-list-timeline'),
    path('groups/timeline/', GroupProfile.as_view(), name='groups-timeline'),
    path('api/pictures', MemberFaceList.as_view(), name='faces-list'),
    path('', MemberFaceIndex.as_view(), name='faces'),
    path('face/add/', MemberFace.as_view(), name='add-face'),
    path('member-autocomplete/', MemberAutoComplete.as_view(),
         name='member-autocomplete'),
    path('api/face', MemberFaceAPI.as_view(), name='member-face'),
    path('admin/', admin.site.urls),
]
