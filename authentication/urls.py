from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', views.user_list, name='register_user'),
    path('user/<str:usr>/', views.single_user_list, name='single_user'),
    path('tenant_list/', views.tenant_list, name='tenant_list'),
    path('landlord_list/', views.landlord_list, name='landlord_list'),
    path('verifyuser/', views.verifyuser, name='verifyuser'),
    path('login/', views.userlogin, name='userlogin'),
    # path('password-reset/', views.password_reset_request, name='password_reset_request'),
    # path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'), 
    path('otp-password-reset/', views.request_otp_password_reset, name='otp-password_reset_request'),
    path('otp-password-reset/confirm/', views.confirm_otp_password_reset, name='otp-password_reset_confirm'), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]

