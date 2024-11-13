from django.db import models
from Traffic_Spots.models import TrafficSpot, PotentialFactor
from django.contrib.auth.models import User

class TrafficAnalysis(models.Model):
    traffic_spot = models.ForeignKey(TrafficSpot, on_delete=models.CASCADE)
    analysis_text = models.TextField()
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Analysis for {self.traffic_spot.title}"

class TrafficHistory(models.Model):
    traffic_spot = models.ForeignKey(TrafficSpot, on_delete=models.CASCADE)
    traffic_level = models.IntegerField()
    factors = models.ManyToManyField(PotentialFactor, blank=True)
    analysis_summary = models.TextField()
    recommendations_summary = models.TextField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"History for {self.traffic_spot.title} on {self.recorded_at}"
