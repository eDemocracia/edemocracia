from django.conf import settings


def settings_variables(request):
    return {
        'SITE_URL': settings.SITE_URL,
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        'OLARK_ID': settings.OLARK_ID,
        'NEW_WIKILEGIS_VISIBLE': settings.NEW_WIKILEGIS_VISIBLE,
        'WIKILEGIS_VISIBLE': settings.WIKILEGIS_VISIBLE,
        'PAUTAS_VISIBLE': settings.PAUTAS_VISIBLE,
        'DISCOURSE_VISIBLE': settings.DISCOURSE_VISIBLE,
        'AUDIENCIAS_VISIBLE': settings.AUDIENCIAS_VISIBLE,
        'CAMARA_LOGIN': settings.CAMARA_LOGIN,
        'PAINEL_PARTICIPACAO_VISIBLE': settings.PAINEL_PARTICIPACAO_VISIBLE,
    }
