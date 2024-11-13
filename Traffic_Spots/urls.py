from django.urls import path
from . import views

app_name = 'Traffic_Spots'

urlpatterns = [
    path('traffic_spots/display/<int:spot_id>/', views.display_traffic_spot, name='display_traffic_spot'),
    path('mark-notification-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]
