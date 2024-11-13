from django.contrib import admin
from .models import TrafficAnalysis, TrafficHistory

@admin.register(TrafficAnalysis)
class TrafficAnalysisAdmin(admin.ModelAdmin):
    list_display = ('traffic_spot', 'created_at', 'created_by')
    search_fields = ('traffic_spot__title',)
    list_filter = ('created_at',)
    readonly_fields = ('created_by',)

@admin.register(TrafficHistory)
class TrafficHistoryAdmin(admin.ModelAdmin):
    list_display = ('traffic_spot', 'traffic_level', 'recorded_at', 'recorded_by')
    search_fields = ('traffic_spot__title',)
    list_filter = ('recorded_at', 'traffic_level')
