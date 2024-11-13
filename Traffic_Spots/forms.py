from django import forms
from .models import TrafficSpot

class TrafficSpotForm(forms.ModelForm):
    location = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = TrafficSpot
        fields = '__all__'
