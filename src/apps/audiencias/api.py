from django.conf import settings
from urllib.parse import urljoin, urlencode


def get_resource_url(resource_name, pk=None):
    api_url = settings.AUDIENCIAS_UPSTREAM + settings.AUDIENCIAS_API_URL

    if resource_name[-1] != '/':
        resource_name += '/'

    resource_url = urljoin(api_url, resource_name)
    if pk is not None:
        resource_url = urljoin(resource_url, pk, allow_fragments=True)

    params = urlencode({'api_key': settings.AUDIENCIAS_API_KEY})

    if resource_url[-1] == '/':
        resource_url = resource_url[:-1]
    return '{}/?{}'.format(resource_url, params)
