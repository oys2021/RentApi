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
from property.serializers import *

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def maintainance(request,usr):
    try:
        tenant = User.objects.get(username=usr, role='Tenant') 
    except User.DoesNotExist:
        return Response({"error": "Tenant with this username does not exist."}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        all_maintainance = MaintenanceRequest.objects.filter(tenant=tenant)
        serializer = MaintenanceRequestSerializer(all_maintainance, many=True,context={'request': request})
        return Response(serializer.data)
    
    elif request.method == "POST":
        data = request.data
        serializer = MaintenanceRequestSerializer(data=data,context={'request': request})
         
        if serializer.is_valid():
            user=serializer.save()
            return Response(
            serializer.data
            ,
    status=status.HTTP_201_CREATED
)
    print("Serializer Errors:",serializer.errors)
    return Response({"error":"Invalid request", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
@permission_classes([AllowAny])
def maintainance_detail(request,usr,id):
    try:
        tenant = User.objects.get(username=usr, role='Tenant') 
    except User.DoesNotExist:
        return Response({"error": "Tenant with this username does not exist."}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        user = MaintenanceRequest.objects.get(tenant=tenant,id=id)
        serializer = MaintenanceRequestSerializer(user,context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        user=MaintenanceRequest.objects.get(tenant=tenant,id=id)
        data=request.data
        serializer = MaintenanceRequestSerializer(user, data=data, partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_property(request,usr):
    if request.method == "GET":
        lease = Lease.objects.get(tenant__username=usr)
        serializer = LeaseSerializer(lease)
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def all_maintainance(request):
    if request.method == "GET":
        all_maintainance = MaintenanceRequest.objects.all()
        serializer = MaintenanceRequestSerializer(all_maintainance, many=True,context={'request': request})
        return Response(serializer.data)