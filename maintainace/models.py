from django.db import models
from authentication.models import *
from property.models import *


import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}')

class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Tenant'})
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title =  models.CharField(max_length=100,null=True)
    attachment = models.FileField(
        upload_to='maintenance_attachments/', 
        blank=True, 
        null=True,
        validators=[validate_file_extension]
    )
    
