from django.urls import path
from .consumer import NotificationConsumer

user_websocket = [
    path('ws/notification/<int:room_id>', NotificationConsumer.as_asgi()),
]
