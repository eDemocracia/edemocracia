from django.conf import settings
import requests


def get_pautas_index_data():
    url = settings.PAUTAS_UPSTREAM + '/api/v1/agenda/'
    params = {'limit': '10', 'order_by': '-end_date'}
    try:
        response = requests.get(url, params=params)
        pautas = response.json()['objects']
    except:
        pautas = []

    return pautas
