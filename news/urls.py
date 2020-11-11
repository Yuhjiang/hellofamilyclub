from rest_framework import routers

from news import views

router = routers.SimpleRouter()

router.register('type', views.NewsTypeViewSet, basename='news-type')
router.register('', views.HelloNewsViewSet, basename='hello-news')

urlpatterns = router.urls
