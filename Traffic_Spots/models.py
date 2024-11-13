from django.db import models
# from Users.models import User
from location_field.models.plain import PlainLocationField 
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.contrib.auth.models import User



class TrafficSpot(models.Model):
    title = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)  # Added city field
    address = models.CharField(_("Traffic Start Address"),max_length=255, default='')
    traffic_start_point = PlainLocationField(based_fields=["city", "address"], zoom=14, default='') 
    end_address = models.CharField(_("Traffic End Address"), max_length=255, default='')
    traffic_end_point = PlainLocationField(based_fields=["city","end_address"], zoom=14, default='') 
    spot_type = models.CharField(max_length=50, choices=[
        ('Turn', 'Turn'),
        ('Main Street/High Street', 'Main Street/High Street'),
        ('Bystreet', 'Bystreet')
    ])
    potential_factors = models.ManyToManyField("PotentialFactor", blank=True)
    traffic_level =  models.CharField(max_length=50, choices=[
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Low', 'Low')
    ], default='High')
    created_at  = models.DateField(_("Appeared In"), default=date.today,)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class PotentialFactor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    message = models.TextField()
    traffic_spot = models.ForeignKey(TrafficSpot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    
    def mark_as_read(self):
        self.is_read = True
        self.save()