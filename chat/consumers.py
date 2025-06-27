import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatModel

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        parts = self.scope["url_route"]["kwargs"]["room_name"].split("_")
        self.user1_id = int(parts[1])
        self.user2_id = int(parts[2])

        # Only allow one of the two users in the room
        if self.scope["user"].id not in [self.user1_id, self.user2_id]:
            await self.close()

        #Generating constan room_name
        self.room_name = f"chat_{min(self.user1_id, self.user2_id)}_{max(self.user1_id, self.user2_id)}"

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    #While getting data from front-end data are in json format and vice versa
    async def receive(self, text_data):
        #Handling Error
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            sender = self.scope["user"]
            sender_id = sender.id

            receiver_id = 0

            #Differentiate sender and receiver
            if sender_id == self.user1_id:
                receiver_id = self.user2_id
            else:
                receiver_id = self.user1_id

            #Saving message
            await self.save_message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message,
                room_name=self.room_name
            )

            #Sending message to room
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender_id,
                    'receiver': receiver_id
                }
            )
        except Exception as e:
            print(f"Error in receive: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Failed to process message'
            }))

    async def chat_message(self, event):
        #Sending message to client
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'receiver': event['receiver']
        }))



    @database_sync_to_async #It is a decorator in django channels. It is used to safely call synchronous Django ORM code from within an asynchronous context as we know our consumer is Async
    def save_message(self, sender_id, receiver_id, message, room_name):
        #Handling Error
        try:
            ChatModel.objects.create(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message,
                room_name=room_name
            )
        except Exception as e:
            print(f"Error in save_message: {e}")