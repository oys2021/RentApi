from property.models import Property,Lease
from rest_framework import serializers
from authentication.models import User 

class PropertySerializer(serializers.ModelSerializer):
    landlord=serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    image_absolute_url = serializers.SerializerMethodField()
 
    class Meta:
        model = Property
        fields = ['id','name','landlord', 'address', 'availability', 'description', 'created_at','image','image_absolute_url']

    def get_image_absolute_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class LeaseSerializer(serializers.ModelSerializer):
    tenant = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username') 

    property = serializers.SlugRelatedField(
        queryset=Property.objects.all(),
        slug_field='name' 
    )

    class Meta:
        model = Lease
        fields = ['id', 'tenant','property', 'start_date', 'end_date', 'rent_amount', 'status']


