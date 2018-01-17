from django.conf import settings
import requests


ERRORS = {
    'missing-input-secret': 'reCAPTCHA: O campo chave está vazio',
    'invalid-input-secret': 'reCAPTCHA: O campo chave está errado ou inválido',
    'missing-input-response': 'reCAPTCHA: O campo de resposta está vazio',
    'invalid-input-response': 'reCAPTCHA: O campo de resposta está errado '
                              'ou inválido',
    'bad-request': 'reCAPTCHA: A requisição está errada ou inválida',
}


def verify(captcha_response, remote_ip=None):
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': captcha_response,
    }

    if remote_ip:
        params['remoteip'] = remote_ip

    verify_response = requests.get(url, params=params, verify=False)
    return verify_response.json()
