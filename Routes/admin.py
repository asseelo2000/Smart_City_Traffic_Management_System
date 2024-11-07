from django.contrib import admin
from .models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "start_location",
        "end_location",
        "estimated_duration",
        "distance",
        "traffic_data_source",
        "is_favorite",
    )
    search_fields = ("start_address", "end_address")

    # class Media:
    #     js = (
    #         'https://maps.googleapis.com/maps/api/js?key=&libraries=places',
    #         "routes/js/user_location.js",
    #     )  # JavaScript file to concatinate city and start_address strings
