from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', views.user_view, name='register_user'),
    path('profile/', views.profile_view, name='tenant_list'),
    path('reset_user/', views.reset_password_view, name='reset_user'),
    path('login/', views.login_view, name='userlogin'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]

