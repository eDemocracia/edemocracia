from django.conf import settings
import requests


def get_wikilegis_index_data():
    url = settings.WIKILEGIS_UPSTREAM + '/api/v1/bill/'
    params = {'limit': '10'}
    try:
        response = requests.get(url, params=params)
        bills = response.json()['objects']
    except:
        bills = []

    return bills
