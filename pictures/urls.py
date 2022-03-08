from django.urls import path, include
from rest_framework.routers import SimpleRouter

from pictures import views

router = SimpleRouter('')
router.register('', views.PictureView, basename='all-picture-view')
router.register('double', views.DoublePictureView,
                basename='double-picture-view')
router.register('group', views.GroupViewSet, basename='group-view')
router.register('all-group', views.GroupListView, basename='all-group-list')
router.register('member', views.MemberViewSet, basename='member-view')
router.register('all-member', views.MemberListView, basename='all-member-list')
router.register('member-face', views.MemberFaceViewSet,
                basename='member-face-view')
router.register('with-member', views.PictureMemberView,
                basename='picture-with-member')
router.register('group-history', views.GroupHistoryView,
                basename='group-history-view')

urlpatterns = [
    path('/cookie', views.WeiboCookieView.as_view(), name='weibo-cookie'),
    path('/recognize', views.RecognizeView.as_view(), name='recognize-view'),
    path('/', include(router.urls)),
]
