from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddleware

from user.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket':
        URLRouter(
            websocket_urlpatterns,
        )
})
