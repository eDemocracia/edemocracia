from apps.core.views import EdemProxyView
from django.conf import settings


class NewWikilegisProxyView(EdemProxyView):
    upstream = settings.NEW_WIKILEGIS_UPSTREAM
    diazo_theme_template = 'diazo-new-wikilegis.html'
    rewrite = (
        (r'/wikilegis/admin/login/?$', '/admin/login'),
        (r'/wikilegis/admin/login/\?([^=\n]+)\=([^&\n]+)$',
         r'/admin/login/?next=\2'),
        (r'/wikilegis/admin/logout/?$', '/admin/logout'),
        (r'/wikilegis/login/?$', '/accounts/login'),
        (r'/wikilegis/login/\?([^=\n]+)\=([^&\n]+)$',
         r'/accounts/login/?next=\2'),
        (r'/wikilegis/logout/?$', '/accounts/logout'),
    )
