from django.db import models
from authentication.models import User


class Notice(models.Model):
    title=models.CharField(max_length=100)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Landlord'})
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)