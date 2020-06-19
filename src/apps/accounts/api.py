from urllib.parse import urlencode, urljoin

import requests

from apps.accounts.serializers import UserSerializer
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet
from django_filters import rest_framework as django_filters
from rest_framework import filters, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from social_django.models import UserSocialAuth


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'last_login': ['lt', 'gt', 'lte', 'gte', 'year__gt', 'year__lt'],
            'date_joined': ['lt', 'gt', 'lte', 'gte', 'year__gt', 'year__lt'],
            'profile__birthdate': ['lt', 'gt', 'lte', 'gte', 'year__gt',
                                   'year__lt'],
            'profile__uf': ['exact'],
            'profile__gender': ['exact'],
            'profile__country': ['exact'],
            'id': ['exact'],
            'email': ['exact'],
        }


class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ('username', 'first_name', 'last_name')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user_list_api',
                         request=request, format=format),
        'participation': request.build_absolute_uri() + 'participation/<UUID>',
    })


@api_view(['GET'])
def get_participation_user(request, user):

    user_auth = UserSocialAuth.get_social_auth('camara_deputados', user)

    if user_auth:
        user = user_auth.user
        response_info = {"username": user.username}
        if project == 'wikilegis':
            response_info['wikilegis'] = get_data_wikilegis(user.username)

        elif project == 'audiencias':
            response_info['audiencias'] = get_data_audiencias(user.username)
        else:
            response_info['wikilegis'] = get_data_wikilegis(user.username)
            response_info['audiencias'] = get_data_audiencias(user.username)

        return Response(response_info)
    else:
        return Response({"error": _("User not found")})


def get_data_audiencias(username):
    api_url_audiencias = (settings.AUDIENCIAS_UPSTREAM
                          + settings.AUDIENCIAS_API_URL)

    url_user = api_url_audiencias + 'user/?username={}'.format(username)
    url_questions = (api_url_audiencias + 
                    'question/?user__username={}'.format(username))
    url_votes = api_url_audiencias + 'vote/?user__username={}'.format(username)
    url_messages = (api_url_audiencias + 
                   'message/?user__username={}'.format(username))

    try:
        response_user = requests.get(url_user)
        if response_user.status_code == 200:
            json_user = response_user.json()
            if json_user['count'] > 0:
                response_question = requests.get(url_questions)
                json_question = response_question.json()

                response_votes = requests.get(url_votes)
                json_votes = response_votes.json()

                response_messages = requests.get(url_messages)
                json_messages = response_messages.json()

                data_audiencias = {
                    "questions_count": json_user['results'][0]
                                                ['questions_count'],
                    "messages_count": json_user['results'][0]
                                                ['messages_count'],
                    "votes_count": json_user['results'][0]['votes_count'],
                    "participations_count": json_user['results'][0]
                    ['participations_count'],
                    "questions_votes_count": json_user['results'][0]
                    ['questions_votes_count'],
                    'questions': json_question['results'],
                    'votes': json_votes['results'],
                    'messages': json_messages['results']}
            else:
                data_audiencias = {'error': _('User not found.')}
        else:
            data_audiencias = {'error': _('API unavailable.')}
    except requests.exceptions.ConnectionError:
        data_audiencias = {'error': _('API unavailable.')}

    return data_audiencias


def get_data_wikilegis(username):
    api_url_wikilegis = (settings.WIKILEGIS_UPSTREAM 
                        + settings.WIKILEGIS_API_URL)

    url_user = api_url_wikilegis + 'api/v1/users/?username={}'.format(username)
    url_graphql = api_url_wikilegis + 'graphql/'

    query = """query{
                user(username: "="){
                    suggestions{
                                id
                                created
                                modified
                                selectedText
                                content
                                author{
                                       firstName
                                      }
                                }
                    votes{
                          suggestion{
                                     id
                                    }
                          opinionVote
                         }
                }
                }
            """
    
    query = query.replace('=', username)

    try:
        response_user = requests.get(url_user)
        if response_user.status_code == 200:
            json_user = response_user.json()
            if json_user['count'] > 0:
                response_participation = requests.post(url_graphql, 
                                                       json={'query': query})
                json_participation = response_participation.json()
                data_wikilegis = {
                    'suggestions_count': json_user['results'][0]
                    ['suggestions_count'],
                    'vote_count': json_user['results'][0]['vote_count'],
                    'votes': json_participation['data']['user']['votes'],
                    'suggestion': json_participation['data']['user']
                                                                ['votes']
                }
            else:
                data_wikilegis = {'error': _('User not found.')}
        else:
            data_wikilegis = {'error': _('API unavailable.')}
    except requests.exceptions.ConnectionError:
        data_wikilegis = {'error': _('API unavailable.')}

    return data_wikilegis
