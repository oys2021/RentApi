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
        is_verified = validated_data.pop('is_verified', True)  
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

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

        user.is_verified = is_verified  

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

class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username does not exist.")
        return value