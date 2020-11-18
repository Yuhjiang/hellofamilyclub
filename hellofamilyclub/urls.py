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
from django.conf import settings

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path('album/', include('album.urls')),
    path('post/', include('blog.urls')),
    path('news/', include('news.urls')),
    path('pictures/', include('pictures.urls')),
    path('user/', include('user.urls')),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
]

schema_view = get_schema_view(
   openapi.Info(
      title="http://hellofamily.club",
      default_version='v1',
      description="HelloFamily接口文档",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

if settings.DEBUG:
    urlpatterns.append(
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
             name='schema-swagger-ui'),
    )

urlpatterns = [
    path('api/v1/', include(urlpatterns)),
]