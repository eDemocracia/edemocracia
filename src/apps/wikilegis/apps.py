from django.apps import AppConfig


class WikilegisConfig(AppConfig):
    name = 'apps.wikilegis'
    verbose_name = 'Wikilegis'

    def ready(self):
        from apps.wikilegis import tasks # noqa
