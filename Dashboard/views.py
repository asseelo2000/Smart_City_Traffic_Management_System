from django.shortcuts import render
from Traffic_Spots.models import TrafficSpot

def index(request):
    # View to count all traffic spots
    spots_count = TrafficSpot.objects.count()  # Use .count() to get the number of objects
    return render(request, 'dashboard/index.html')

def live_traffic_map(request):
    # View to display the Google Maps integration
    return render(request, 'dashboard/live_traffic_map.html')

def traffic_spots_list(request):
    # View to list all traffic spots
    spots = TrafficSpot.objects.all()
    return render(request, 'dashboard/traffic_spots_list.html', {'spots': spots})