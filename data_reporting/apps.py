from django.apps import AppConfig


class DataReportingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_reporting'

    def ready(self):
        from . import signals
