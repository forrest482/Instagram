import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.other_user = self.scope['url_route']['kwargs']['username']

        # Sort the usernames alphabetically for a consistent room name
        room_users = sorted([self.user.username, self.other_user])
        self.room_group_name = f'chat_{"_".join(room_users)}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(
            f"Received message from {self.scope['user'].username} is {text_data}")

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['from']
        receiver_username = text_data_json['to']

        # Verify that the sender_id corresponds to an existing user
        if not await self.is_valid_user(sender_id):
            print(f"Invalid sender_id: {sender_id}")
            return  # Optionally, handle this situation more gracefully

        # Save the message
        saved_message = await self.save_message(sender_id, receiver_username, message)

        message_data = {
            'id': saved_message.id,
            'content': saved_message.content,
            'timestamp': saved_message.timestamp.isoformat(),
            'read': saved_message.read,
            'sender': saved_message.sender.id,
            'receiver': saved_message.receiver.id
        }

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_data
            }
        )

    async def chat_message(self, event):
        message = event['message']
        print(f"Sending message to WebSocket: {message}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_username, content):
        print(
            f"save_message: {sender_id} - {receiver_username} - {content}")

        from .models import Message
        from django.contrib.auth import get_user_model

        User = get_user_model()

        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(username=receiver_username)

        message = Message.objects.create(
            sender=sender, receiver=receiver, content=content)
        print("saved:", message)
        return message

    @database_sync_to_async
    def is_valid_user(self, user_id):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        return User.objects.filter(id=user_id).exists()
