"""
URL configuration for Core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    
    path('traffic-super/', admin.site.urls),
    path('users/', include('Users.urls', namespace='users')),  # Make sure this includes the Users app URLs
    path('dashboard/', include('Dashboard.urls', namespace='dashboard')),  # Dashboard URLs
    path('traffic_spots/', include('Traffic_Spots.urls')),

    # Redirect the root URL to the login page
    path('', lambda request: redirect('users:login')),
    ]