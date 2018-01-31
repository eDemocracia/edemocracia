from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import requests
import json

from apps.audiencias.apps import AudienciasConfig
from apps.audiencias.api import get_resource_url
from apps.core.tasks import default_login
from apps.core.utils import get_user_data


@receiver(user_logged_in)
def audiencias_login(sender, user, request, **kwargs):
    default_login(user, request, AudienciasConfig)


@receiver(user_logged_out)
def audiencias_logout(sender, user, request, **kwargs):
    request.delete_cookies.append(AudienciasConfig.cookie_name)


@receiver(post_save, sender=User)
def update_audiencias_user(sender, instance, created, **kwargs):
    data = get_user_data(instance)
    data['username'] = instance.username

    response = requests.put(get_resource_url('user', pk=instance.username),
                            data=json.dumps(data),
                            headers={'Content-Type': 'application/json'})
    if response.status_code == 404:
        requests.post(get_resource_url('user'), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})


@receiver(post_delete, sender=User)
def delete_audiencias_user(sender, instance, **kwargs):
    requests.delete(get_resource_url('user', pk=instance.username))
