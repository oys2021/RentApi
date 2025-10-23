from django.urls import path
from . import views


urlpatterns = [
    path('property/<str:usr>/', views.property_view, name='property'),
    path('property_detail/<int:id>/', views.property_detail_view, name='property_detail'),
    path('lease/', views.lease_view, name='lease'),
    path('lease_detail/<int:id>/',views.lease_detail_view, name='lease_detail'),
    path('tenant_property/',views.tenant_property_view, name='tenant_property')
    
]

