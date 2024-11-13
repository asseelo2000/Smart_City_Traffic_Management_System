from django.shortcuts import render, get_object_or_404
from .models import TrafficAnalysis, TrafficHistory

def index(request):
    # View to list all traffic analyses
    analyses = TrafficAnalysis.objects.all()
    return render(request, 'traffic_analysis/index.html', {'analyses': analyses})

def analysis_detail(request, analysis_id):
    # View to display details of a specific traffic analysis
    analysis = get_object_or_404(TrafficAnalysis, id=analysis_id)
    return render(request, 'traffic_analysis/detail.html', {'analysis': analysis})

def traffic_history(request):
    # View to display historical traffic data
    history = TrafficHistory.objects.all()
    return render(request, 'traffic_analysis/history.html', {'history': history})
