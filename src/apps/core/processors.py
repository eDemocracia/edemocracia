from django.conf import settings


def settings_variables(request):
    return {
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        'OLARK_ID': settings.OLARK_ID,
        'WIKILEGIS_ENABLED': settings.WIKILEGIS_ENABLED,
        'PAUTAS_ENABLED': settings.PAUTAS_ENABLED,
    }


def home_customization(request):
    return {'site_name': settings.SITE_NAME, 'site_logo': settings.SITE_LOGO}
