from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from apps.core.tasks import default_login


@receiver(user_logged_in)
def wikilegis_login(sender, user, request, **kwargs):
    default_login(user, request, upstream=settings.WIKILEGIS_UPSTREAM,
                  cookie_name='wikilegis_session')
