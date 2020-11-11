from rest_framework import routers

from user import views

router = routers.SimpleRouter()

router.register('', views.UserViewSet, basename='user')

urlpatterns = router.urls
