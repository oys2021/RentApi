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
from authentication.utils import send_code_to_user,send_reset_otp_to_user,generate_and_store_otp
from django.contrib.auth.hashers import make_password

import random



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_list(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        data = request.data
        if User.objects.filter(username=data.get('username')).exists():
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=data.get('email')).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=data)
        print(serializer)
         
        if serializer.is_valid():
            user=serializer.save()
            print("to email",serializer.data["email"])
            send_code_to_user(serializer.data["email"])
            
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
    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def tenant_list(request):
    if request.method == "GET":
        users = User.objects.filter(role="Tenant")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def landlord_list(request):
    if request.method == "GET":
        users = User.objects.filter(role="Landlord")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def verifyuser(request):
    if request.method == "POST":
        otpdata=request.data.get("otp")
        try:
            user_code_obj=OneTimePassword.objects.get(code=otpdata)
            user=user_code_obj.user
            if not user.is_verified:
                user.is_verified =True
                user.save()
                return Response({
                    'message':'email account verified successfully'
                },status=status.HTTP_200_OK)
            return Response({
                    'message':'code is invalid user verified already'
                },status=status.HTTP_204_NO_CONTENT)
        
        except OneTimePassword.DoesNotExist:
            return Response({
                    'message':'passcode not provided'
                },status=status.HTTP_404_NOT_FOUND)
            
@api_view(['POST'])
@permission_classes([AllowAny])
def userlogin(request):
    if request.method == "POST":
        data = request.data
        username = data.get("username")
        password = data.get("password")
        
        user = authenticate(username=username, password=password)
        user_role=User.objects.get(username=username)
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



# @api_view(['POST'])
# def password_reset_request(request):
#     serializer = PasswordResetRequestSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.send_reset_email()
#         return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def password_reset_confirm(request):
#     serializer = PasswordResetSerializer(data=request.data)
#     if serializer.is_valid():
#         return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def request_otp_password_reset(request):
    serializer = PasswordOtpResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp_code = generate_and_store_otp(email)
        print("Great otp",otp_code)
        send_reset_otp_to_user(email,otp_code)
        
        return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
    
    print("Serializer Errors:", serializer.errors)
    return Response({"error": "Invalid request", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def confirm_otp_password_reset(request):
    serializer = PasswordOtpResetConfirmSerializer(data=request.data)
    
    if serializer.is_valid():
        otp_code = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]

        try:
            otp_verify = OneTimePassword.objects.get(code=otp_code, used=False)  # Ensure OTP is not used
            user = otp_verify.user

            user.password = make_password(new_password)
            user.save()

            otp_verify.used = True
            otp_verify.save()

            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        
        except OneTimePassword.DoesNotExist:
            return Response({"error": "Invalid OTP or OTP already used."}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "Invalid request", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
@permission_classes([AllowAny])
def single_user_list(request,usr):
    if request.method == "GET":
        user = User.objects.get(username=usr)
        serializer = UserSerializer(user,context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        user=User.objects.get(username=usr)
        data=request.data
        serializer = UserSerializer(user, data=data, partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            