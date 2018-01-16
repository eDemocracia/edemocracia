from apps.core.views import EdemProxyView
from django.conf import settings


class WikilegisProxyView(EdemProxyView):
    upstream = settings.WIKILEGIS_UPSTREAM
    diazo_theme_template = 'diazo-base.html'
