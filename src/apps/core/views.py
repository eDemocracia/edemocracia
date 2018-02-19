from django.conf import settings
from revproxy.views import DiazoProxyView
from django.shortcuts import render
import requests
import json
from datetime import datetime, timedelta

from apps.discourse.data import get_discourse_index_data
from apps.wikilegis.data import get_wikilegis_index_data
from apps.pautas.data import get_pautas_index_data


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
    context = {}
    if settings.PAUTAS_ENABLED:
        context['pautas'] = get_pautas_index_data()

    if settings.WIKILEGIS_ENABLED:
        context['bills'] = get_wikilegis_index_data()

    if settings.DISCOURSE_ENABLED:
        context['topics'] = get_discourse_index_data()

    if settings.AUDIENCIAS_ENABLED:
        audiencias_url = settings.AUDIENCIAS_UPSTREAM + '/api/room/'
        today = datetime.today().strftime('%Y-%m-%d')
        tomorrow = (datetime.today() + timedelta(1)).strftime('%Y-%m-%d')
        today_params = {'date__gte': today, 'date__lt': tomorrow,
                        'is_visible': 'True', 'ordering': '-date'}
        today_response = requests.get(
            audiencias_url, params=today_params)
        today_rooms = today_response.json()['results']
        live_rooms = [x for x in today_rooms if x['youtube_status'] == 1]
        history_rooms = [x for x in today_rooms if x['youtube_status'] == 2]
        agenda_rooms = [x for x in today_rooms if x['youtube_status'] == 0]

        if len(today_rooms) == 0:
            history_params = {
                'youtube_status': 2, 'ordering': '-date'}
            history_response = requests.get(
                audiencias_url, params=history_params)
            history_rooms = history_response.json()['results'][:10]
        elif len(today_rooms) < 10:
            diff_cards = 10 - len(today_rooms)
            agenda_params = {
                'date__gte': today, 'youtube_status': 0, 'ordering': 'date'}
            agenda_response = requests.get(
                audiencias_url, params=agenda_params)
            extra_agenda_rooms = agenda_response.json()['results'][:diff_cards]
            agenda_rooms = agenda_rooms + extra_agenda_rooms

        context['history_rooms'] = history_rooms
        context['agenda_rooms'] = agenda_rooms
        context['live_rooms'] = live_rooms

    return render(request, 'index.html', context)
