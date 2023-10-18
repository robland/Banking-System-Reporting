from django.apps import AppConfig


class DataImportationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_importation'

    def ready(self):
        from . import signals

