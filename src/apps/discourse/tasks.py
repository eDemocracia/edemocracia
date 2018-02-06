from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from pydiscourse.sso import sso_validate, sso_redirect_url
import requests
import re


@receiver(user_logged_in)
def discourse_login(sender, user, request, **kwargs):
    upstream = settings.DISCOURSE_UPSTREAM
    upstream = upstream[:-1] if upstream[-1] == '/' else upstream

    response = requests.get(upstream + '/session/sso', allow_redirects=False)
    if response.status_code == 302:
        location = response.headers['Location']

        regex = re.compile(r'sso=(.+)&sig=(.+)')
        matches = regex.search(location)
        payload, signature = matches.groups()
        secret = settings.DISCOURSE_SSO_SECRET

        nonce = sso_validate(payload, signature, secret)
        url = sso_redirect_url(nonce, secret, user.email, user.id,
                               user.username,
                               name=user.get_full_name().encode('utf-8'))
        response = requests.get(upstream + url, allow_redirects=False)
        t_cookie = response.cookies.get('_t')

        request.COOKIES['_t'] = t_cookie


@receiver(user_logged_out)
def discourse_logout(sender, user, request, **kwargs):
    request.delete_cookies.append('_forum_session')
    request.delete_cookies.append('_t')
