from apps.core.views import EdemProxyView
from django.conf import settings


class WikilegisProxyView(EdemProxyView):
    upstream = settings.WIKILEGIS_UPSTREAM
    diazo_theme_template = 'diazo-wikilegis.html'
    rewrite = (
        (r'/wikilegis-arquivo/admin/login/?$', '/admin/login'),
        (r'/wikilegis-arquivo/admin/login/\?([^=\n]+)\=([^&\n]+)$',
         r'/admin/login/?next=\2'),
        (r'/wikilegis-arquivo/admin/logout/?$', '/admin/logout'),
        (r'/wikilegis-arquivo/login/?$', '/accounts/login'),
        (r'/wikilegis-arquivo/login/\?([^=\n]+)\=([^&\n]+)$',
         r'/accounts/login/?next=\2'),
        (r'/wikilegis-arquivo/logout/?$', '/accounts/logout'),
    )
