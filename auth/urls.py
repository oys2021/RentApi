from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.user_list, name='register_user'),
]

