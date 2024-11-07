import os
import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import models
from Users.models import User
from location_field.models.plain import PlainLocationField 


# Model for storing information about routes.
class Route(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='routes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routes')
    city = models.CharField(max_length=100, blank=True, null=True)  # Added city field
    start_address = models.CharField(max_length=255, blank=True)  # Optional address field if needed
    start_location = PlainLocationField(based_fields=["city","start_address"], zoom=14, default='') 
    end_address = models.CharField(max_length=255, blank=True)  # Optional address field if needed
    end_location = PlainLocationField(based_fields=["city","end_address"],zoom=14, default='')   
    estimated_duration = models.DurationField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)  # distance in kilometers
    traffic_data_source = models.CharField(max_length=100, choices=[('Google Maps', 'Google Maps'), ('OpenStreetMap', 'OpenStreetMap')])
    is_favorite = models.BooleanField(default=False)

    def calculate_distance_using_google(self):
        # Get the API key from environment variables or settings
        # api_key = os.getenv('GOOGLE_MAPS_API') or settings.GOOGLE_API_KEY
        api_key = settings.GOOGLE_API_KEY

        # Format the coordinates for the API request
        if self.start_location and self.end_location:
            start_lat, start_lon = map(float, self.start_location.split(','))
            end_lat, end_lon = map(float, self.end_location.split(','))
            origin = f"{start_lat},{start_lon}"
            destination = f"{end_lat},{end_lon}"

            # Construct the API request URL
            url = (
                f"https://maps.googleapis.com/maps/api/distancematrix/json"
                f"?origins={origin}&destinations={destination}&key={api_key}"
            )

            # Make the API request
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                try:
                    # Extract the distance in kilometers
                    distance_meters = data['rows'][0]['elements'][0]['distance']['value']
                    distance_km = distance_meters / 1000  # Convert meters to kilometers
                    return distance_km
                except (IndexError, KeyError):
                    return 0
        return 0
    
        
    def __str__(self):
        return f"Route from {self.start_location} to {self.end_location} by {self.user.username}"

    def save(self, *args, **kwargs):
        # Calculate and set the distance before saving
        self.distance = self.calculate_distance_using_google()
        super().save(*args, **kwargs)