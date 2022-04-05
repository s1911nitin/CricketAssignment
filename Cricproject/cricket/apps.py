from django.apps import AppConfig


class CricketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cricket'

    def ready(self):
        import cricket.signals