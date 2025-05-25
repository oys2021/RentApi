from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import *
from authentication.models import *
import json
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.core.cache import cache

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name=f'chat__{self.room_name}'
        
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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_username = text_data_json['sender_username']
        receiver_username = text_data_json['receiver_username']

        sender = await self.get_user(user_name=sender_username)
        receiver = await self.get_user(user_name=receiver_username)

        if not sender or not receiver:
            print("Sender or receiver not found")
            return

        timestamp = await self.save_message(sender, receiver, message, self.room_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'receiver': receiver.username,
                'timestamp': timestamp,
            }
        )

        user = await sync_to_async(User.objects.get)(username=receiver)

        notification = await sync_to_async(Notification.objects.create)(
            user=user,
            message=f'New message from {sender}: {message}',
        )
        
        notification_count = await sync_to_async(Notification.objects.filter(user__username=receiver, read=False).count)()


        await self.channel_layer.group_send(
            f'notifications_{receiver}',
            {
                'type': 'send_notification',
                'message': notification.message,
                'count': notification_count,
            }
        )



    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        timestamp = event.get('timestamp', None)  

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver,
            'timestamp': timestamp  
        }))
        
    # async def send_notification(self, event):
    #     message = event['message']
    #     count = event['count']

    #     await self.send(text_data=json.dumps({
    #         'type': 'notification',
    #         'message': message,
    #         'count': count,
    #     }))


    @sync_to_async
    def get_user(self, user_name):
        try:
            return User.objects.get(username=user_name)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def save_message(self, sender, receiver, message, room_name):
        msg = Message.objects.create(
            sender=sender,
            receiver=receiver,
            message=message,
            room_name=room_name
        )
        return msg.timestamp.isoformat()  


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'notifications_{self.user_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        message = event['message']
        count = event['count']
        

        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
            'count': count,
        }))