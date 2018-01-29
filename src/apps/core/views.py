from django.shortcuts import render
from revproxy.views import DiazoProxyView
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
    pautas_url = 'http://localhost:8000/pautaparticipativa/api/v1/agenda/'
    pautas_params = {'limit': '10', 'order_by': '-end_date'}
    pautas_response = requests.get(pautas_url, params=pautas_params)
    pautas_data = json.loads(pautas_response.text)
    pautas = pautas_data['objects']
    wikilegis_url = 'http://localhost:8000/wikilegis/api/v1/bill/'
    wikilegis_params = {'limit': '10'}
    wikilegis_response = requests.get(wikilegis_url, params=wikilegis_params)
    wikilegis_data = json.loads(wikilegis_response.text)
    bills = wikilegis_data['objects']
    return render(request, 'index.html', {
        'pautas': pautas,
        'bills': bills
    })
