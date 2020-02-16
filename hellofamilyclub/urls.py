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
from django.urls import path

from pictures.views import MemberFaceAPI, MemberFace, MemberFaceIndex, \
    MemberFaceList, GroupProfile, MemberFaceListDate
from pictures.autocomplete import MemberAutoComplete

urlpatterns = [
    path('api/pictures/timeline/', MemberFaceListDate.as_view(),
         name='faces-list-timeline'),
    path('groups/profile/', GroupProfile.as_view(), name='groups-profile'),
    path('api/pictures/', MemberFaceList.as_view(), name='faces-list'),
    path('', MemberFaceIndex.as_view(), name='faces'),
    path('face/add/', MemberFace.as_view(), name='add-face'),
    path('member-autocomplete/', MemberAutoComplete.as_view(),
         name='member-autocomplete'),
    path('api/face/', MemberFaceAPI.as_view(), name='member-face'),
    path('admin/', admin.site.urls),
]
