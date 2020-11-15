from typing import List

from rest_framework import routers
from django.urls import path

from pictures import views

router = routers.SimpleRouter()

router.register('carousel', views.CarouselPictureViewSet, basename='carousel')
router.register('group', views.GroupViewSet, basename='group')
router.register('member', views.MemberViewSet, basename='member')

urlpatterns: List = router.urls

urlpatterns.extend(
    [
        path('/', views.MemberFaceList.as_view(), name='picture-list'),
        path('recognize/', views.RecognizePicture.as_view(),
             name='recognize-picture'),
        path('download/', views.DownloadPictures.as_view(),
             name='download-picture'),
        path('cookie/', views.CookieAPI.as_view(), name='cookie'),
        path('timeline/', views.MemberFaceListDate.as_view(),
             name='picture-list-timeline'),
        path('face/', views.MemberFaceAPI.as_view(), name='member-face'),
    ]
)