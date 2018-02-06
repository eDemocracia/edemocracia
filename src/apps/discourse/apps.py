from django.apps import AppConfig
from django.conf import settings


class DiscourseConfig(AppConfig):
    name = 'apps.discourse'

    def ready(self):
        if settings.DISCOURSE_ENABLED:
            from apps.discourse import tasks # noqa