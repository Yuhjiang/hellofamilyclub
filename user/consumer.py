import asyncio
import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.generic.http import AsyncHttpConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(self.channel_name)
        text_data_json = json.loads(text_data)
        message = '测试：' + text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message,
        }))

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_group_name = 'hellofamily'
#
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name)
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = '测试：' + text_data_json['message']
#
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     def chat_message(self, event):
#         message = 'hello: ' + event['message']
#
#         self.send(text_data=json.dumps({
#             'message': message
#         }))


class ServerSentEventsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        while True:
            data = datetime.now().isoformat()
            print(data)
            await self.send(text_data=json.dumps({
                'message': data,
            }))
            await asyncio.sleep(10)

# class ServerSentEventsConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, code):
#         pass
#
#     def receive(self, text_data=None, bytes_data=None):
#         while True:
#             data = datetime.now().isoformat()
#             print(data)
#             self.send(text_data=json.dumps({
#                 'message': data,
#             }))
#             asyncio.sleep(1)


if __name__ == '__main__':
    chatroom = ChatConsumer()
    chatroom.send(text_data=json.dumps({'message': '123'}))