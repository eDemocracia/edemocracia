from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import requests
import json


@receiver(user_logged_in)
def wikilegis_login(sender, user, request, **kwargs):
    user_data = {
        'name': user.first_name,
        'email': user.email,
    }
    headers = {'Auth-User': user.username,
               'Remote-User-Data': json.dumps(user_data)}
    response = requests.get(settings.WIKILEGIS_UPSTREAM, headers=headers)

    if response.status_code == 200:
        session = response.cookies.get('wikilegis_session')
        request.COOKIES['wikilegis_session'] = session
