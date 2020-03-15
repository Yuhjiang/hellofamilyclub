from channels.routing import ProtocolTypeRouter, URLRouter

from user.routing import user_websocket

application = ProtocolTypeRouter({
    'websocket': URLRouter(user_websocket)
})