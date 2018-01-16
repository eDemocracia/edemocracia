from revproxy.views import DiazoProxyView
from django.conf import settings


class WikilegisProxyView(DiazoProxyView):
    upstream = settings.WIKILEGIS_UPSTREAM
    diazo_theme_template = 'diazo-base.html'
    html5 = True
