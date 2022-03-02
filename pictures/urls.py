from django.urls import path, include
from rest_framework.routers import SimpleRouter

from pictures import views

router = SimpleRouter('')
router.register('', views.PictureView, basename='all-picture-view')
router.register('group', views.GroupViewSet, basename='group-view')
router.register('member', views.MemberViewSet, basename='member-view')
router.register('member-face', views.MemberFaceViewSet,
                basename='member-face-view')
router.register('with-member', views.PictureMemberView,
                basename='picture-with-member')

urlpatterns = [
    path('cookie', views.WeiboCookieView.as_view(), name='weibo-cookie'),
    path('/', include(router.urls)),
]
