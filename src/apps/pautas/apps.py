from django.apps import AppConfig
from django.conf import settings


class PautasConfig(AppConfig):
    name = 'apps.pautas'
    verbose_name = 'Pauta Participativa'
    cookie_name = 'pautas_session'
    upstream = settings.PAUTAS_UPSTREAM

    def ready(self):
        if settings.PAUTAS_ENABLED:
            from apps.pautas import tasks # noqa
