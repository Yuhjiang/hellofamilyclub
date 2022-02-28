from django.urls import path

from pictures import views

urlpatterns = [
    path('cookie', views.WeiboCookieView.as_view(), name='weibo-cookie')
]
