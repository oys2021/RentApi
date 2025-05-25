from django.db import models

# Create your models here.
from authentication.models import User

class Property(models.Model):
    name=models.CharField(max_length=100,null=True)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Landlord'})
    address = models.TextField()
    availability = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(
        upload_to='properties/', 
        blank=True, 
        null=True,
    )
    
    def __str__(self):
        return self.name

class Lease(models.Model):
    tenant = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lease', limit_choices_to={'role': 'Tenant'})
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('expired', 'Expired')])

    def __str__(self):
        return f"Lease for {self.tenant.username} at {self.property.name}"

