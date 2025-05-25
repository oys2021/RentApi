from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import  Response
from rest_framework import status
from authentication.models import *
from authentication.serializer import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from maintainace.models import *
from maintainace.serializers import *
from notice.serializers import *
from notice.models import *

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def notice(request,usr):
    try:
        landlord = User.objects.get(username=usr, role='Landlord') 
    except User.DoesNotExist:
        return Response({"error": "Landlord with this username does not exist."}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        all_notices = Notice.objects.filter(landlord=landlord)
        serializer = NoticeSerializer(all_notices, many=True,context={'request': request})
        return Response(serializer.data)
    
    elif request.method == "POST":
        data = request.data
        serializer = NoticeSerializer(data=data,context={'request': request})
         
        if serializer.is_valid():
            user=serializer.save()
            return Response(
            serializer.data
            ,
    status=status.HTTP_201_CREATED
)
    print("Serializer Errors:",serializer.errors)
    return Response({"error":"Invalid request", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from property.models import Lease

@api_view(['GET'])
@permission_classes([AllowAny])
def landlord(request, usr):
    if request.method == "GET":
        lease = Lease.objects.filter(tenant__username=usr).select_related('property__landlord').first()

        if not lease:
            return Response({"error": "Landlord not found for this tenant"}, status=404)

        landlord = lease.property.landlord  
        
        landlord_details = {
            'username': landlord.username,
            'name': landlord.get_full_name() if hasattr(landlord, 'get_full_name') else landlord.username,
            'email': landlord.email,
            'phone': getattr(landlord, 'phone', None)  
        }

        return Response(landlord_details)
