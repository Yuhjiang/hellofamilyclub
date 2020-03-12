from django.urls import path
from .consumer import ChatConsumer, ServerSentEventsConsumer

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer),
    path('ws/time/', ServerSentEventsConsumer)
]
