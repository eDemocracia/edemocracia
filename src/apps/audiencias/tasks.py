from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from apps.audiencias.apps import AudienciasConfig
from apps.core.tasks import default_login


@receiver(user_logged_in)
def audiencias_login(sender, user, request, **kwargs):
    default_login(user, request, AudienciasConfig)
