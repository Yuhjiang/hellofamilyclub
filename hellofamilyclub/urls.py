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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from album.apis import AlbumViewSet
from blog.apis import PostViewSet, CategoryViewSet, TagViewSet, upload_picture, \
    CommentViewSet
from news.apis import NewsTypeViewSet, HelloNewsViewSet
from pictures.apis import CarouselPictureViewSet, GroupViewSet, MemberViewSet, \
    RecognizePicture, DownloadPictures
from user.apis import login_user, register_user, UserViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='api-post')
router.register(r'category', CategoryViewSet, basename='api-category')
router.register(r'tag', TagViewSet, basename='api-tag')
router.register(r'user', UserViewSet, basename='api-user')
router.register(r'carousel', CarouselPictureViewSet, basename='api-carousel')
router.register(r'group', GroupViewSet, basename='api-group')
router.register(r'member', MemberViewSet, basename='api-member')
router.register(r'comment', CommentViewSet, basename='api-comment')
router.register(r'newstype', NewsTypeViewSet, basename='api-news-type')
router.register(r'hellonews', HelloNewsViewSet, basename='api-hello-news')
router.register(r'album', AlbumViewSet, basename='api-album')

base_urlpatterns = [
    path('recognize_picture/', RecognizePicture.as_view(),
         name='recognize-picture'),
    path('download_pictures/', DownloadPictures.as_view(),
         name='download-picuturs'),
    path('upload_picture', upload_picture, name='upload-picture'),
    path('', include(router.urls)),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('user', include('user.urls')),
    path('picture', include('pictures.urls')),
]

urlpatterns = [
    path('api/v1/', include(base_urlpatterns))
]
