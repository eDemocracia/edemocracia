from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import requests
import json
import logging
from apps.core.tasks import default_login
from apps.core.utils import get_user_data
from apps.pautas.apps import PautasConfig
from apps.pautas.api import get_resource_url


@receiver(user_logged_in)
def pautas_login(sender, user, request, **kwargs):
    try:
        default_login(user, request, PautasConfig)
    except requests.exceptions.ConnectionError:
        logging.exception("Can't login in Pautas")


@receiver(user_logged_out)
def pautas_logout(sender, user, request, **kwargs):
    request.delete_cookies.append('pautas_session')


@receiver(post_save, sender=User)
def update_pautas_user(sender, instance, created, **kwargs):
    data = get_user_data(instance)
    data.pop('username', None)
    try:
        requests.put(get_resource_url('user', pk=instance.username),
                    data=json.dumps(data),
                    headers={'Content-Type': 'application/json'})
    except requests.exceptions.ConnectionError:
        logging.exception("Pautas Connection refused")


@receiver(post_delete, sender=User)
def delete_pautas_user(sender, instance, **kwargs):
    requests.delete(get_resource_url('user', pk=instance.username),
                    headers={'Content-Type': 'application/json'})
