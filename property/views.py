from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import  Response
from rest_framework import status
from authentication.models import *
from authentication.serializer import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from property.models import *
from property.serializers import *
from django.db import IntegrityError

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def property_view(request):
    landlord=request.user

    if request.method == "GET":
        all_properties = Property.objects.filter(landlord=landlord) 
        serializer = PropertySerializer(all_properties, many=True,context={'request': request})
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        data["landlord"] = landlord  
        serializer = PropertySerializer(data=data,context={'request': request})
         
        if serializer.is_valid():
            property_instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("Serializer Errors:", serializer.errors)
        return Response({"error": "Invalid request", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def property_detail_view(request,id):
    landlord=request.user
    if request.method == "GET":
        user = Property.objects.get(landlord=landlord, id=id)
        serializer = PropertySerializer(user,context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        user=Property.objects.get(landlord=landlord,id=id)
        data=request.data
        serializer = PropertySerializer(user, data=data, partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lease_view(request):
    tenant = request.user
    if request.method == "GET":
        all_properties = Lease.objects.filter(tenant=tenant)
        serializer = LeaseSerializer(all_properties, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        
        if Lease.objects.filter(tenant=tenant, property__name=data.get('property')).exists():
            return Response(
                {"error": "A lease already exists for this tenant and property combination."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = LeaseSerializer(data=data)
        
        if serializer.is_valid():
            try:
                lease = serializer.save()
                return Response(LeaseSerializer(lease).data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"error": "A lease with this tenant and property already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response({"error": "Invalid request", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def lease_detail_view(request,usr):
    tenant=request.user
    if request.method == "GET":
        user = Lease.objects.get(tenant=tenant,id=id)
        serializer = LeaseSerializer(user,context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        user=Lease.objects.get(tenant=tenant)
        data=request.data
        serializer = LeaseSerializer(user, data=data, partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
            
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_property_view(request,usr):
    if request.method == "GET":
        lease = Lease.objects.get(tenant__username=usr)
        serializer = LeaseSerializer(lease)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tenant_property_view(request,usr):
    tenant = request.user
    if request.method == "GET":
        try:  
            leases = Lease.objects.filter(tenant = tenant).select_related('property')
            
            property_details = []
            for lease in leases:
                property_details.append({
                    'property_name': lease.property.name, 
                    'address': lease.property.address,
                    'image': request.build_absolute_uri(lease.property.image.url) if lease.property.image else None,  
                    'rent_amount': lease.rent_amount,
                    'status': lease.status,
                    'start_date': lease.start_date,
                    'end_date': lease.end_date,
                })
            return Response(property_details)
        
        except Lease.DoesNotExist:
            return Response({"error": "Lease not found for this tenant"}, status=404)


