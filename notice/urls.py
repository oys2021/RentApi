from django.urls import path
from . import views


urlpatterns = [
    path('notice/<str:usr>/', views.notice, name='notice'),
    path('landlord/<str:usr>/', views.landlord, name='landlord'),
]

