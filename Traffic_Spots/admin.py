from django.contrib import admin
from Core.settings import OPENAI_API_KEY
from Traffic_Analysis_and_Reommendations.models import TrafficAnalysis
from Traffic_Spots.forms import TrafficSpotForm
from .models import Notification, TrafficSpot, PotentialFactor

from django.contrib import messages
import requests
import json
from django.conf import settings

from openai import OpenAI

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('traffic_spot', 'is_read')
    readonly_fields = ('traffic_spot','is_read')


@admin.register(TrafficSpot)
class TrafficSpotAdmin(admin.ModelAdmin):
    form = TrafficSpotForm
    class Media:
        js = (
            'https://maps.googleapis.com/maps/api/js?key=AIzaSyCI1s4gfgAJhKJQA19Ff2Uv4NBwsdXBFpQ&libraries=places',
            'js/google_traffic_map.js',
        )
    change_form_template = 'traffic-super/Traffic_Spots/TrafficSpot/change_form.html'

    # class Media:
    #     js = ('https://maps.googleapis.com/maps/api/js?key=AIzaSyCI1s4gfgAJhKJQA19Ff2Uv4NBwsdXBFpQ&libraries=places', 'js/google_traffic_map.js')
    
    list_display = ('title', 'city', 'address', 'spot_type', 'created_by')
    search_fields = ('title', 'city', 'address')
    readonly_fields = ('created_by',)
    list_filter = ('spot_type', 'city')
    actions = ['analyze_traffic']

    def save_model(self, request, obj, form, change):
        if not obj.created_by:  # Only set 'created_by' if it hasn't been set
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def analyze_traffic(self, request, queryset):
        # Check if the OpenAI API key is in settings
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if not api_key:
            self.message_user(request, "OpenAI API key is not configured.", level=messages.ERROR)
            return

        for traffic_spot in queryset:
            # Prepare data from the TrafficSpot object
            title = traffic_spot.title
            city = traffic_spot.city
            traffic_start_point = traffic_spot.traffic_start_point  # Assuming these are coordinates
            traffic_end_point = traffic_spot.traffic_end_point    # Assuming these are coordinates
            spot_type = traffic_spot.spot_type
            potential_factors = ', '.join([factor.name for factor in traffic_spot.potential_factors.all()])
            traffic_level = traffic_spot.traffic_level

            # Prepare the request payload for OpenAI
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            f"Analyze the traffic situation at {title} in {city}. "
                            f"The spot is a {spot_type} between {traffic_start_point} and {traffic_end_point}. "
                            f"Potential traffic factors include: {potential_factors}. "
                            f"Traffic level is: {traffic_level}. "
                            "Provide a short analysis and recommendations to improve the traffic conditions."
                        )
                    }
                ],
                "temperature": 0.7
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            # Make the API call to OpenAI
            try:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload)
                ) 
                response_data = response.json()

                # Extract analysis and recommendations from the response
                if response.status_code == 200:
                    content = response_data.get("choices", [])[0].get("message", {}).get("content", "No analysis provided.")
                    # Split the content into analysis and recommendations
                    analysis, recommendations = self._parse_response(content)

                    # Create and save a TrafficAnalysis object in the Traffic_Analysis_and_Recommendations app
                    TrafficAnalysis.objects.create(
                        traffic_spot=traffic_spot,
                        analysis_text=analysis,
                        recommendations=recommendations,
                        created_by=request.user  # Assuming 'request.user' is a User instance
                    )

                    self.message_user(request, f"Analysis for {title} saved successfully.", level=messages.SUCCESS)
                else:
                    error_message = response_data.get("error", {}).get("message", "Unknown error occurred.")
                    self.message_user(request, f"Error for {title}: {error_message}", level=messages.ERROR)

            except requests.exceptions.RequestException as e:
                self.message_user(request, f"Request failed for {title}: {str(e)}", level=messages.ERROR)

    analyze_traffic.short_description = "Analyze traffic using OpenAI"

    # Helper method to parse the API response into analysis and recommendations
    def _parse_response(self, content):
        # This is a simple example of parsing. Adjust it based on your response format.
        if "Recommendations:" in content:
            parts = content.split("Recommendations:")
            analysis = parts[0].strip()
            recommendations = parts[1].strip()
        else:
            analysis = content
            recommendations = "No specific recommendations provided."

        return analysis, recommendations



@admin.register(PotentialFactor)
class PotentialFactorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    