from rest_framework import routers

from album import views

router = routers.SimpleRouter()
router.register(r'album', views.AlbumViewSet, basename='album')
router.register(r'picture', views.PictureViewSet, basename='picture')


urlpatterns = router.urls
