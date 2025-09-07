import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ShoppingSession

User = get_user_model()

class ShoppingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'shopping_{self.room_name}'
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send user joined notification
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'user': self.user.email if self.user.is_authenticated else 'Anonymous',
                'message': f'{self.user.email if self.user.is_authenticated else "Anonymous"} joined the session'
            }
        )

    async def disconnect(self, close_code):
        # Send user left notification
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'user': self.user.email if self.user.is_authenticated else 'Anonymous',
                'message': f'{self.user.email if self.user.is_authenticated else "Anonymous"} left the session'
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'chat_message')
        
        if message_type == 'chat_message':
            message = data['message']
            user = self.user.email if self.user.is_authenticated else 'Anonymous'
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user,
                    'timestamp': data.get('timestamp')
                }
            )
        
        elif message_type == 'product_share':
            product = data['product']
            user = self.user.email if self.user.is_authenticated else 'Anonymous'
            
            # Send product share to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'product_share',
                    'product': product,
                    'user': user
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        timestamp = event.get('timestamp')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'user': user,
            'timestamp': timestamp
        }))

    async def product_share(self, event):
        product = event['product']
        user = event['user']

        # Send product share to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'product_share',
            'product': product,
            'user': user
        }))

    async def user_joined(self, event):
        # Send user joined notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'user': event['user'],
            'message': event['message']
        }))

    async def user_left(self, event):
        # Send user left notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'user': event['user'],
            'message': event['message']
        }))

    @database_sync_to_async
    def get_session(self, session_id):
        try:
            return ShoppingSession.objects.get(session_id=session_id, is_active=True)
        except ShoppingSession.DoesNotExist:
            return None