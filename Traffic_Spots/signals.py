from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import TrafficSpot, Notification

@receiver(post_save, sender=TrafficSpot)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification when a new TrafficSpot is created
        Notification.objects.create(
            message=f"New traffic spot '{instance.title}' created in {instance.city}.",
            traffic_spot=instance
        )

@receiver(pre_delete, sender=TrafficSpot)
def create_notification_on_delete(sender, instance, **kwargs):
        print(f"Deleting TrafficSpot: {instance.title}")  # Debug statement

        # Create a notification before the TrafficSpot is deleted
        Notification.objects.create(
            message=f"Traffic spot '{instance.title}' in {instance.city} is about to be disappeared.",
            traffic_spot=instance
        )