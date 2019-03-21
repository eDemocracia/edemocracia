from django.conf import settings
from urllib.parse import urljoin, urlencode


def get_resource_url(resource_name, pk=None):
    api_url = urljoin(
        settings.NEW_WIKILEGIS_UPSTREAM, settings.NEW_WIKILEGIS_API_URL)

    if resource_name[-1] != '/':
        resource_name += '/'

    resource_url = urljoin(api_url, resource_name)
    if pk is not None:
        resource_url = urljoin(resource_url, pk, allow_fragments=True)

    params = urlencode({'api_key': settings.NEW_WIKILEGIS_API_KEY})

    return '{}/?{}'.format(resource_url, params)
