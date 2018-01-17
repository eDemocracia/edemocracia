from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from apps.core.tasks import default_login
from apps.wikilegis.apps import WikilegisConfig


@receiver(user_logged_in)
def wikilegis_login(sender, user, request, **kwargs):
    default_login(user, request, WikilegisConfig)


@receiver(user_logged_out)
def wikilegis_logout(sender, user, request, **kwargs):
    request.delete_cookies.append('wikilegis_session')
