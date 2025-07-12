from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'
 # properties/apps.py

    def ready(self):
        import properties.signals  # noqa
