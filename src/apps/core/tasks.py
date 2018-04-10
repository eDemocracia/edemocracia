from apps.core.utils import get_user_data
import requests
import json


def default_login(user, request, app_config):

    headers = {'Auth-User': user.username,
               'Remote-User-Data': json.dumps(get_user_data(user))}
    response = requests.get(app_config.upstream, headers=headers)

    if response.status_code == 200:
        session = response.cookies.get(app_config.cookie_name)
        request.COOKIES[app_config.cookie_name] = session
