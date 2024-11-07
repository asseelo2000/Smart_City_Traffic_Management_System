from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FavoriteLocation

@admin.register(FavoriteLocation)
class FavoriteLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'address', 'city', 'location', 'added_on')
    search_fields = ('name', 'address', 'city')

