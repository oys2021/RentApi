from django.shortcuts import render
from rest_framework.response import  Response
from rest_framework import status
from authentication.models import *
from authentication.serializer import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum
from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from django.contrib.auth.hashers import make_password
import random



@api_view(['POST'])
@permission_classes([AllowAny])
def user_view(request):
    if request.method == "POST":
        data = request.data
        if User.objects.filter(username=data.get('username')).exists():
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=data.get('email')).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=data)
        print(serializer)
         
        if serializer.is_valid():
            user=serializer.save()

            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return Response(
            {
                **serializer.data, 
                'access': str(access),
                'refresh': str(refresh),
            },
    status=status.HTTP_201_CREATED
)
    print("Serializer Errors:", serializer.errors)
    return Response({"error": "Invalid request", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def profile_view(request):
    if request.method == "GET":
        users = User.objects.filter(role="Tenant")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    
            
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == "POST":
        data = request.data
        username = data.get("username")
        password = data.get("password")
        
        user = authenticate(username=username, password=password)
        try:
            user_role=User.objects.get(username=username)
        
        except User.DoesNotExist:
            return Response({"error": "User Does not Exist."}, status=status.HTTP_404_NOT_FOUND)
        print(user_role.role)
        
        if not user:
            return Response({"error": "Invalid credentials. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_verified:
            return Response({"error": "Username is not verified."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LoginSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({
                "message": "Login Successful",
                "access_token": serializer.validated_data['access_token'],
                "refresh_token": serializer.validated_data['refresh_token'],
                "role":user_role.role
            }, status=status.HTTP_200_OK)

        return Response({
            "error": "Invalid request",
            "details": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_view(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


