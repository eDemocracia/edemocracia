from datetime import datetime
from requests import request, HTTPError
from django.core.files.base import ContentFile


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        user.profile.gender = response.get('gender', '')
        birthdate = response.get('birthday', '')
        if birthdate:
            user.profile.birthdate = datetime.strptime(birthdate, '%m/%d/%Y')
        location = response.get('location', '')
        if location:
            user.profile.country = location['name'].split(', ')[1]
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
        try:
            response_image = request('GET', url, verify=False)
            response_image.raise_for_status()
        except HTTPError:
            pass
        else:
            user.profile.avatar.save('{0}_fb.jpg'.format(user.username),
                                     ContentFile(response_image.content))

    if backend.name == 'google-oauth2':
        user.profile.gender = response.get('gender', '')
        if not response.get('image').get('isDefault'):
            url = response.get('image').get('url').replace('?sz=50', '?sz=200')
            try:
                response_image = request('GET', url, verify=False)
                response_image.raise_for_status()
            except HTTPError:
                pass
            else:
                user.profile.avatar.save('{0}_g.jpg'.format(user.username),
                                         ContentFile(response_image.content))
