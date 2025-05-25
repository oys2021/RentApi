from maintainace.models import MaintenanceRequest
from rest_framework import serializers
from chat.models import *


class MessagesSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username') 
    receiver = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username') 
        
    class Meta:
        model = Message
        fields = ['id','sender','receiver','message', 'room_name', 'timestamp']

   

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username') 
    class Meta:
        model = Notification
        fields = ['id','user', 'message', 'read', 'created_at']