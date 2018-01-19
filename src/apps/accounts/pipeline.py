from datetime import datetime
from requests import request, HTTPError
from django.core.files.base import ContentFile


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'camara_deputados':
        user.profile.uf = response.get('uf', '')
        user.profile.gender = response.get('sexo', '')
        user.profile.country = response.get('pais', '')
        user.profile.birthdate = response.get('dataNascimento', '')
        if user.profile.avatar:
            user.profile.save()
        else:
            url = response.get('foto', '')
            try:
                response_image = request('GET', url, verify=False)
                response_image.raise_for_status()
            except HTTPError:
                pass
            else:
                user.profile.avatar.save('{0}_cd.jpg'.format(user.username),
                                         ContentFile(response_image.content))

    if backend.name == 'facebook':
        if 'email' in response.get('denied_scopes', '') and not user.email:
            user.email = response.get('id') + '@facebook.com'
            user.save()
        user.profile.gender = response.get('gender', '')
        birthdate = response.get('birthday', '')
        if birthdate:
            user.profile.birthdate = datetime.strptime(birthdate, '%m/%d/%Y')
        location = response.get('location', '')
        if location:
            user.profile.country = location['name'].split(', ')[1]
        if user.profile.avatar:
            user.profile.save()
        else:
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
        if response.get('image').get('isDefault') or user.profile.avatar:
            user.profile.save()
        else:
            url = response.get('image').get('url').replace('?sz=50', '?sz=200')
            try:
                response_image = request('GET', url, verify=False)
                response_image.raise_for_status()
            except HTTPError:
                pass
            else:
                user.profile.avatar.save('{0}_g.jpg'.format(user.username),
                                         ContentFile(response_image.content))
