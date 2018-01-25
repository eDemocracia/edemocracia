from django.conf import settings


def recaptcha_site_key(request):
    return {'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY}


def home_customization(request):
    return {'site_name': settings.SITE_NAME, 'site_logo': settings.SITE_LOGO}
