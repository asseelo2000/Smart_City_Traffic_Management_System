from django.db import models
from Users.models import User
from location_field.models.plain import PlainLocationField
from django.utils.translation import gettext_lazy as _

# Model for user's favorite locations.
class FavoriteLocation(models.Model):
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)  # Added city field
    location = PlainLocationField(based_fields=['address'], zoom=7)  # Added location field with map integration
    name = models.CharField(_("Alternate Name"),max_length=255)  # Friendly name for the location
    added_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Favorite {self.name} for {self.user.username}"