from django.apps import AppConfig
from django.conf import settings


class WikilegisConfig(AppConfig):
    name = 'apps.wikilegis'
    verbose_name = 'Wikilegis'
    cookie_name = 'wikilegis_session'
    upstream = settings.WIKILEGIS_UPSTREAM

    def ready(self):
        from apps.wikilegis import tasks # noqa
