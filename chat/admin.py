from django.contrib import admin
from chat.models import Message,Notification
# Register your models here.
admin.site.register(Message)
admin.site.register(Notification)
