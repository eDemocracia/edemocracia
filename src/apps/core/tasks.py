import requests
import json


def default_login(user, request, cookie_name='', upstream=''):
    if cookie_name == '' or upstream == '':
        raise ValueError('cookie_name and upstream should not be empty')

    user_data = {
        'name': user.first_name,
        'email': user.email,
    }

    headers = {'Auth-User': user.username,
               'Remote-User-Data': json.dumps(user_data)}
    response = requests.get(upstream, headers=headers)

    if response.status_code == 200:
        session = response.cookies.get(cookie_name)
        request.COOKIES[cookie_name] = session
