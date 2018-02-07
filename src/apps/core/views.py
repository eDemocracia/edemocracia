from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from revproxy.views import DiazoProxyView
from django.shortcuts import render
import requests
import json


class EdemProxyView(DiazoProxyView):
    html5 = True

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        if request.user.is_authenticated:
            user_data = {
                'name': request.user.first_name,
                'email': request.user.email,
            }

            request.META['HTTP_REMOTE_USER_DATA'] = json.dumps(user_data)

        return super(EdemProxyView, self).dispatch(request, *args, **kwargs)


def index(request):
    site = get_current_site(request)
    context = {}
    if settings.PAUTAS_ENABLED:
        pautas_url = site.domain + '/pautaparticipativa/api/v1/agenda/'
        pautas_params = {'limit': '10', 'order_by': '-end_date'}
        pautas_response = requests.get(pautas_url, params=pautas_params)
        pautas_data = json.loads(pautas_response.text)
        pautas = pautas_data['objects']
        context['pautas'] = pautas
    if settings.WIKILEGIS_ENABLED:
        wikilegis_url = settings.WIKILEGIS_UPSTREAM + '/api/v1/bill/'
        wikilegis_params = {'limit': '10'}
        wikilegis_response = requests.get(wikilegis_url,
                                          params=wikilegis_params)
        wikilegis_data = json.loads(wikilegis_response.text)
        bills = wikilegis_data['objects']
        context['bills'] = bills

    if settings.DISCOURSE_ENABLED:
        categories_url = settings.DISCOURSE_UPSTREAM + '/categories.json'
        categories = requests.get(categories_url).json()
        categories = categories['category_list']['categories']

        latest_url = settings.DISCOURSE_UPSTREAM + '/latest.json'
        latest = requests.get(latest_url).json()
        latest = latest['topic_list']['topics']

        context['topics'] = []
        for topic in latest[:10]:
            topic_category = None

            for category in categories:
                if category['id'] == topic['category_id']:
                    topic_category = category

            topic['category_name'] = topic_category['name']
            topic['category_slug'] = topic_category['slug']

            context['topics'].append(topic)

    return render(request, 'index.html', context)
