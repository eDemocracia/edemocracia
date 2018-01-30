from django.apps import AppConfig
from django.conf import settings


class AudienciasConfig(AppConfig):
    name = 'apps.audiencias'
    verbose_name = 'Audiências Interativas'
    cookie_name = 'audiencias_session'
    upstream = settings.AUDIENCIAS_UPSTREAM + '/audiencias'

    def ready(self):
        if settings.AUDIENCIAS_ENABLED:
            from apps.audiencias import tasks # noqa
