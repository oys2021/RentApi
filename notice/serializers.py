from notice.models import *
from rest_framework import serializers
from authentication.models import User 


class NoticeSerializer(serializers.ModelSerializer):
    landlord=serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
 
    class Meta:
        model = Notice
        fields = "__all__"
