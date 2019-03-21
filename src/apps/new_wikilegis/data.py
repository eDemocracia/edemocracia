from django.conf import settings
import requests


def get_new_wikilegis_index_data():
    url = (settings.NEW_WIKILEGIS_UPSTREAM +
           settings.NEW_WIKILEGIS_API_URL + 'groups/')
    response = requests.get(url)
    documents = response.json()['results']

    return documents
