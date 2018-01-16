import requests
import json


def default_login(user, request, app_config):

    user_data = {
        'name': user.first_name,
        'email': user.email,
    }

    headers = {'Auth-User': user.username,
               'Remote-User-Data': json.dumps(user_data)}
    response = requests.get(app_config.upstream, headers=headers)

    if response.status_code == 200:
        session = response.cookies.get(app_config.cookie_name)
        request.COOKIES[app_config.cookie_name] = session
