import asyncio
import json
from datetime import datetime

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.generic.http import AsyncHttpConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = '测试：' + text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message,
        }))


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