from django.shortcuts import redirect, render, get_object_or_404
from Traffic_Analysis_and_Reommendations.models import TrafficAnalysis
from .models import Notification, TrafficSpot


def display_traffic_spot(request, spot_id):
    spot = get_object_or_404(TrafficSpot, id=spot_id)
    traffic_analysis = TrafficAnalysis.objects.filter(traffic_spot=spot).first()  # Fetch the related TrafficAnalysis object
    return render(request, 'traffic_spots/display_traffic_spot.html', {
        'spot': spot,
        'traffic_analysis': traffic_analysis,
    })

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.mark_as_read()
    return redirect('Traffic_Spots:display_traffic_spot', notification.traffic_spot.id)

# def traffic_spot_detail(request, spot_id):
#     # View to display details of a specific traffic spot
#     spot = get_object_or_404(TrafficSpot, id=spot_id)
#     return render(request, 'traffic_spots/detail.html', {'spot': spot})