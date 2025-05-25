from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from authentication.utils import send_code_to_user,send_password_request_to_user

class UserSerializer(serializers.ModelSerializer):
    image_absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone', 'image', 'image_absolute_url','created_at','role','firstname','lastname','is_verified']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_image_absolute_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        phone = validated_data.pop('phone', None)
        role = validated_data.pop('role', None)
        firstname = validated_data.pop('firstname', None)
        lastname = validated_data.pop('lastname', None)
        is_verified = validated_data.pop('is_verified', False)  # Default to False if not provided
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Set additional fields
        if image:
            user.image = image

        if phone:
            user.phone = phone

        if role:
            user.role = role

        if firstname:
            user.firstname = firstname

        if lastname:
            user.lastname = lastname

        user.is_verified = is_verified  # Ensure is_verified is stored

        user.save()
        return user

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        phone = validated_data.pop('phone', None)
        role = validated_data.pop('role', None)
        

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if image is not None:
            instance.image = image
        
        if phone is not None:
            instance.phone = phone
            
        if role is not None:
            instance.role = role
        
        instance.save()
        return instance
    
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=155)
    password=serializers.CharField(max_length=68, write_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['password', 'username', 'access_token', 'refresh_token']

    

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        request=self.context.get('request')
        user = authenticate(request, username=username, password=password)
        if not user:
            raise AuthenticationFailed("invalid credential try again")
        if not user.is_verified:
            raise AuthenticationFailed("username is not verified")
        tokens=user.tokens()
        return {
            'username':user.username,
            "access_token":str(tokens.get('access')),
            "refresh_token":str(tokens.get('refresh'))
        }




# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         if not User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("No account found with this email.")
#         return value

#     def send_reset_email(self):
#         # from django.core.mail import send_mail

#         email = self.validated_data['email']
#         user = User.objects.get(email=email)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         token = default_token_generator.make_token(user)
#         reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"
#         send_password_request_to_user(email,reset_link)
        
# class PasswordResetSerializer(serializers.Serializer):
#     uid = serializers.CharField()
#     token = serializers.CharField()
#     new_password = serializers.CharField(write_only=True, min_length=6)

#     def validate(self, data):
#         from django.utils.http import urlsafe_base64_decode
#         from django.contrib.auth.tokens import default_token_generator

#         try:
#             uid = urlsafe_base64_decode(data['uid']).decode()
#             user = User.objects.get(pk=uid)
#         except (User.DoesNotExist, ValueError, TypeError):
#             raise serializers.ValidationError("Invalid reset link.")

#         if not default_token_generator.check_token(user, data['token']):
#             raise serializers.ValidationError("Invalid or expired token.")

#         user.set_password(data['new_password'])
#         user.save()
#         return data
    

class PasswordOtpResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email.")
        return value
    



class PasswordOtpResetConfirmSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Invalid OTP format. It should be a 6-digit number.")
        return value

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value