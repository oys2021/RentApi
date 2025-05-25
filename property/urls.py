from django.urls import path
from . import views


urlpatterns = [
    path('property/<str:usr>', views.property, name='property'),
    path('property_detail/<str:usr>/<int:id>', views.property_detail, name='property_detail'),
    path('lease/<str:usr>', views.lease, name='lease'),
    path('leases/', views.all_lease, name='leases'),
    path('lease_detail/<str:usr>/<int:id>',views.lease_detail, name='lease_detail'),
    path('tenant_property/<str:usr>/',views.tenant_property, name='tenant_property')
    
]

