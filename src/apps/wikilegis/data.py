from django.conf import settings
import requests


def get_wikilegis_index_data():
    url = settings.WIKILEGIS_UPSTREAM + '/api/v1/bill/'
    params = {'limit': '10'}
    response = requests.get(url, params=params)
    bills = response.json()['objects']

    return bills
