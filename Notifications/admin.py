from django.contrib import admin
from .models import TrafficNotification

@admin.register(TrafficNotification)
class TrafficNotificationAdmin(admin.ModelAdmin):
    list_display = ('route', 'message', 'timestamp', 'severity_level', 'is_active')
    list_filter = ('severity_level', 'is_active')
