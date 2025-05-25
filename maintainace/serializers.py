from maintainace.models import MaintenanceRequest
from rest_framework import serializers
from maintainace.models import *
from property.models import *


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    tenant = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username') 
    file_absolute_url = serializers.SerializerMethodField()
    property = serializers.SlugRelatedField(
        queryset=Property.objects.all(),
        slug_field='name' 
    )
    
    class Meta:
        model = MaintenanceRequest
        fields = ['id','title','tenant','property', 'description', 'priority', 'status', 'created_at', 'updated_at','attachment','file_absolute_url']

    def get_file_absolute_url(self, obj):
        request = self.context.get('request')
        if obj.attachment and request:
            return request.build_absolute_uri(obj.attachment.url)
        return None
