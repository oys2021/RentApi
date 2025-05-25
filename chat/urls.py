from django.urls import path
from . import views


urlpatterns = [
    path('messages/<str:room_name>/', views.messages, name='messages'),
    path('notifications/<str:user_id>/', views.get_notifications, name='get-notifications'),
    path('notifications/mark-as-read/<str:user_id>/', views.mark_notifications_as_read, name='mark-notifications-as-read'),
    path('notifications/count/<str:user_id>/', views.get_notification_count, name='notification-count'),
    # path('notifications/reset/<int:user_id>/', views.reset_notification_count, name='notification-reset'),
]

