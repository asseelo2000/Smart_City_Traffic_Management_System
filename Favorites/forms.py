from django import forms
from .models import FavoriteLocation

class FavoriteLocationForm(forms.ModelForm):
    class Meta:
        model = FavoriteLocation
        fields = ['name', 'address', 'location']