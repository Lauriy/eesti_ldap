import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class BirthdayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        year = int(self.scope['url_route']['kwargs']['year'])
        month = int(self.scope['url_route']['kwargs']['month'])
        day = int(self.scope['url_route']['kwargs']['day'])
        # TODO: Better validation? Through forms?
        # TODO: get_or_create? Then we can't use AsyncWebsocketConsumer or must use async_to_sync
        datetime.date(year, month, day)
        # self.username = await database_sync_to_async(self.get_name)()
        self.date_group_name = 'birthdate_%d_%d_%d' % (year, month, day)

        # Join date group
        await self.channel_layer.group_add(
            self.date_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.date_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.date_group_name,
            {
                'type': 'birthdate.message',
                'message': message
            }
        )

    # Receive message from date group
    async def birthdate_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))
