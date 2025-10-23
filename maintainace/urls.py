from django.urls import path
from . import views


urlpatterns = [
    path('maintainance/', views.maintainance_view, name='maintainance'),
    path('user_property/', views.user_property_view, name='user_property'),
    path('maintainance_detail/<int:id>/', views.maintainance_detail_view, name='maintainance_detail'),
]

