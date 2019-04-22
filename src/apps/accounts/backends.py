from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from social_core.backends.oauth import BaseOAuth2
from django.conf import settings
from apps.accounts.models import generate_username


class CamaraOAuth2(BaseOAuth2):
    name = 'camara_deputados'
    AUTHORIZATION_URL = settings.CAMARA_DEPUTADOS_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.CAMARA_DEPUTADOS_ACCESS_TOKEN_URL
    METADATA_URL = settings.CAMARA_DEPUTADOS_METADATA_URL
    ACCESS_TOKEN_METHOD = 'POST'
    DEFAULT_SCOPE = ['openid']

    def get_user_details(self, response):
        email = response.get('email')
        nome = response.get('nome')
        if nome == email:
            nome = generate_username(email)
        return {'username': generate_username(email),
                'email': email,
                'first_name': nome}

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json(self.METADATA_URL, headers={
            'Authorization': 'Bearer %s' % access_token
        })

    def auth_complete_credentials(self):
        return self.get_key_and_secret()


class AuthenticationEmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if (getattr(user, 'is_active', False) and
                    user.check_password(password)):
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
