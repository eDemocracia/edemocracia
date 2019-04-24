from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import requests
import json

from apps.core.tasks import default_login
from apps.core.utils import get_user_data
from apps.new_wikilegis.apps import NewWikilegisConfig
from apps.new_wikilegis.api import get_resource_url


@receiver(user_logged_in)
def new_wikilegis_login(sender, user, request, **kwargs):
    default_login(user, request, NewWikilegisConfig)


@receiver(user_logged_out)
def new_wikilegis_logout(sender, user, request, **kwargs):
    request.delete_cookies.append(NewWikilegisConfig.cookie_name)


@receiver(post_save, sender=User)
def update_new_wikilegis_user(sender, instance, created, **kwargs):
    data = get_user_data(instance)

    requests.put(get_resource_url('users', pk=instance.username),
                 data=json.dumps(data),
                 headers={'Content-Type': 'application/json'})


@receiver(post_delete, sender=User)
def delete_new_wikilegis_user(sender, instance, **kwargs):
    requests.delete(get_resource_url('user', pk=instance.username),
                    headers={'Content-Type': 'application/json'})
