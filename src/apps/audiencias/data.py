from django.conf import settings
from datetime import datetime, timedelta
import requests


def get_audiencias_index_data():
    url = settings.AUDIENCIAS_UPSTREAM + '/api/room/'
    today = datetime.today().strftime('%Y-%m-%d')
    tomorrow = (datetime.today() + timedelta(1)).strftime('%Y-%m-%d')
    today_params = {'date__gte': today, 'date__lt': tomorrow,
                    'is_visible': 'True', 'ordering': '-date'}
    today_response = requests.get(
        url, params=today_params)
    today_rooms = today_response.json()['results']
    live_rooms = [x for x in today_rooms if x['youtube_status'] == 1]
    history_rooms = [x for x in today_rooms if x['youtube_status'] == 2]
    agenda_rooms = [x for x in today_rooms if x['youtube_status'] == 0]

    if len(today_rooms) == 0:
        agenda_params = {
            'date__gte': today, 'youtube_status': 0, 'ordering': 'date',
            'is_visible': 'True'}
        agenda_response = requests.get(
            url, params=agenda_params)
        extra_agenda_rooms = agenda_response.json()['results'][:10]
        agenda_rooms = agenda_rooms + extra_agenda_rooms

        diff_cards = 10 - len(agenda_rooms)
        history_params = {
            'youtube_status': 2, 'ordering': '-date'}
        history_response = requests.get(
            url, params=history_params)
        history_rooms = history_response.json()['results'][:diff_cards]
    elif len(today_rooms) < 10:
        diff_cards = 10 - len(today_rooms)
        agenda_params = {
            'date__gte': today, 'youtube_status': 0, 'ordering': 'date',
            'is_visible': 'True'}
        agenda_response = requests.get(
            url, params=agenda_params)
        extra_agenda_rooms = agenda_response.json()['results'][:diff_cards]
        agenda_rooms = agenda_rooms + extra_agenda_rooms
    rooms = {}
    rooms['history_rooms'] = history_rooms
    rooms['agenda_rooms'] = agenda_rooms
    rooms['live_rooms'] = live_rooms

    return rooms
