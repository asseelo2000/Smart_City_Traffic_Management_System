from django.apps import AppConfig


class TrafficSpotsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Traffic_Spots'

    def ready(self):
        import Traffic_Spots.signals  # Import the signals