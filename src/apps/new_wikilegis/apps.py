from django.apps import AppConfig
from django.conf import settings


class NewWikilegisConfig(AppConfig):
    name = 'apps.new_wikilegis'
    verbose_name = 'New Wikilegis'
    cookie_name = 'new_wikilegis_session'
    upstream = settings.NEW_WIKILEGIS_UPSTREAM

    def ready(self):
        if settings.NEW_WIKILEGIS_ENABLED:
            from apps.new_wikilegis import tasks # noqa
