from django.shortcuts import render
from chat.models import *
from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import  Response
from rest_framework import status
from authentication.models import *
from chat.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from maintainace.models import *
from maintainace.serializers import *
from property.serializers import *
from rest_framework import generics, permissions
from django.core.cache import cache


# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def messages(request,room_name):
    if request.method == "GET":
        messages = Message.objects.filter(room_name=room_name)
        serializer = MessagesSerializer(messages, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_notifications(request, user_id):
    notifications = Notification.objects.filter(user__username=user_id).order_by('-created_at')[:10]  
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def mark_notifications_as_read(request, user_id):
    Notification.objects.filter(user__username=user_id, read=False).update(read=True)
    return Response({'status': 'success'})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_notification_count(request, user_id):
    count = Notification.objects.filter(user__username=user_id, read=False).count()
    return Response({'count': count})

