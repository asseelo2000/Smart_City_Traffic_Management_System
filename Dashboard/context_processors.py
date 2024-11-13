from Traffic_Analysis_and_Reommendations.models import TrafficAnalysis
from Traffic_Spots.models import Notification, TrafficSpot

def all_apps_context(request):
    # Count the number of TrafficAnalysis objects
    traffic_analysis_count = TrafficAnalysis.objects.count()
    spots = TrafficSpot.objects.all()
    spots_count = TrafficSpot.objects.count()  # Use .count() to get the number of objects
    notifications = Notification.objects.filter(is_read=False)

    return {
        'user': request.user,
        'traffic_analysis_count': traffic_analysis_count,
        'spots': spots,
        'spots_count': spots_count,
        'notifications': notifications
    }
