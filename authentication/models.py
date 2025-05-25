from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Landlord', 'Landlord'),
        ('Tenant', 'Tenant'),
        ('Admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='Tenant')
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    phone=models.CharField(max_length=15,null=True,blank=True)
    firstname=models.CharField(max_length=35,null=True,blank=True)
    lastname=models.CharField(max_length=35,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_verified=models.BooleanField(default=False)
    
    def tokens(self):    
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }

    def __str__(self):
        return self.username
    
class OneTimePassword(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    code=models.CharField(max_length=6,unique=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    used = models.BooleanField(default=False,null=True)
    
    def __str__(self):
        return f"{self.user.username} - passcode"
    
    

    
    
