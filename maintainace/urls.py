from django.urls import path
from . import views


urlpatterns = [
    path('maintainance/<str:usr>/', views.maintainance, name='maintainance'),
    path('all_maintainance/', views.all_maintainance, name='all_maintainance'),
    path('user_property/<str:usr>/', views.user_property, name='user_property'),
    path('maintainance_detail/<str:usr>/<int:id>/', views.maintainance_detail, name='maintainance_detail'),
]

