from django.conf import settings
from revproxy.views import DiazoProxyView
from django.shortcuts import render
import json

from apps.discourse.data import get_discourse_index_data
from apps.wikilegis.data import get_wikilegis_index_data
from apps.new_wikilegis.data import get_new_wikilegis_index_data
from apps.pautas.data import get_pautas_index_data
from apps.audiencias.data import get_audiencias_index_data
from apps.core.utils import get_user_data
import requests
import logging

def get_painel_audiencias_data():
    reports_api_url = (settings.AUDIENCIAS_UPSTREAM +
                       '/reports/api/')
    try:
        rooms_response = requests.get(reports_api_url +
                                      'rooms/?period=yearly')
        total_rooms = rooms_response.json()['sum_total_results']
    except:
        logging.exception("Connection refused in url "
                          "%srooms/?period=yearly" % reports_api_url)
        total_rooms = '-' # Server Error
    
    try:
        participants_response = requests.get(
            reports_api_url + 'participants/?period=all')
        total_participants = participants_response.json()['sum_total_results']
    except:
        logging.exception("Connection refused in url "
                          "%sparticipants/?period=al" % reports_api_url)
        total_participants = '-' # Server Error

    return total_rooms, total_participants


def get_painel_wikielgis_data():
    reports_api_url = (settings.NEW_WIKILEGIS_UPSTREAM +
                       '/reports/api/')
    try:
        documents_response = requests.get(reports_api_url +
                                          'documents/?period=yearly')
        total_documents = documents_response.json()['sum_total_results']
    except:
        logging.exception("Connection refused in url "
                          "%sdocuments/?period=yearly" % reports_api_url)
        total_documents = '-' # Server Error
    
    try:
        participants_response = requests.get(
            reports_api_url + 'participants/?period=all')
        total_participants = participants_response.json()['sum_total_results']
    except:
        logging.exception("Connection refused in url "
                          "%sparticipants/?period=all" % reports_api_url)
        total_participants = '-' # Server Error

    return total_documents, total_participants


class EdemProxyView(DiazoProxyView):
    html5 = True

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        if request.user.is_authenticated:
            user_data = get_user_data(request.user)
            request.META['HTTP_REMOTE_USER_DATA'] = json.dumps(user_data)

        return super(EdemProxyView, self).dispatch(request, *args, **kwargs)


def index(request):
    context = {}
    if settings.PAUTAS_VISIBLE:
        context['pautas'] = get_pautas_index_data()

    if settings.NEW_WIKILEGIS_VISIBLE:
        context['groups'] = get_new_wikilegis_index_data()

    if settings.WIKILEGIS_VISIBLE:
        context['bills'] = get_wikilegis_index_data()

    if settings.DISCOURSE_VISIBLE:
        context['topics'] = get_discourse_index_data()

    if settings.AUDIENCIAS_VISIBLE:
        rooms = get_audiencias_index_data()

        if rooms == 500: # Server Error
            context['status_code'] = rooms
        else:
            context['status_code'] = 200 # Request OK
            context['history_rooms'] = rooms['history_rooms']
            context['agenda_rooms'] = rooms['agenda_rooms']
            context['live_rooms'] = rooms['live_rooms']

    if settings.PAINEL_PARTICIPACAO_VISIBLE:
        total_audiencias_rooms, total_audiencias_participants = get_painel_audiencias_data()
        total_wikilegis_documents, total_wikilegis_participants = get_painel_wikielgis_data()

        context['total_audiencias_rooms'] = total_audiencias_rooms
        context['total_audiencias_participants'] = total_audiencias_participants
        context['total_wikilegis_documents'] = total_wikilegis_documents
        context['total_wikilegis_participants'] = total_wikilegis_participants

    return render(request, 'index.html', context)
