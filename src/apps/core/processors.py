from django.conf import settings


def settings_variables(request):
    return {
        'SITE_URL': settings.SITE_URL,
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        'OLARK_ID': settings.OLARK_ID,
        'WIKILEGIS_ENABLED': settings.WIKILEGIS_ENABLED,
        'PAUTAS_ENABLED': settings.PAUTAS_ENABLED,
        'DISCOURSE_ENABLED': settings.DISCOURSE_ENABLED,
        'AUDIENCIAS_ENABLED': settings.AUDIENCIAS_ENABLED,
        'CAMARA_LOGIN': settings.CAMARA_LOGIN,
    }
