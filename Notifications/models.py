from django.db import models
from Routes.models import Route

# Model for traffic notifications along routes.
class TrafficNotification(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    severity_level = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Moderate', 'Moderate'), ('High', 'High')])
    is_active = models.BooleanField(default=True)  # Determines if the notification is still relevant
    
    def __str__(self):
        return f"Notification for {self.route} - {self.severity_level}"