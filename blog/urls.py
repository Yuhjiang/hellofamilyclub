from django.urls import path

from rest_framework import routers

from blog import views

router = routers.SimpleRouter()
router.register('', views.PostViewSet, basename='post')
router.register('category', views.CategoryViewSet, basename='category')
router.register('tag', views.CategoryViewSet, basename='tag')
router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = router.urls

urlpatterns.append(
    path('upload_picture/', views.upload_picture, name='upload_picture')
)