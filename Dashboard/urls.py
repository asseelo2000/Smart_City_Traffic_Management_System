from django.urls import path
from . import views

app_name = 'Dashboard'
urlpatterns = [
    path('', views.index, name='index'),  
    path('live_traffic_map/', views.live_traffic_map, name='live_traffic_map'),
    path('traffic_spots_list/', views.traffic_spots_list, name='traffic_spots_list'),
]
