from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:analysis_id>/', views.analysis_detail, name='analysis_detail'),
    path('history/', views.traffic_history, name='traffic_history'),
]
