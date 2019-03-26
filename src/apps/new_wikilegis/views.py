from apps.core.views import EdemProxyView
from django.conf import settings


class NewWikilegisProxyView(EdemProxyView):
    upstream = settings.NEW_WIKILEGIS_UPSTREAM
    diazo_theme_template = 'components/diazo-base.html'
    rewrite = (
        (r'/new-wikilegis/admin/login/?$', '/admin/login'),
        (r'/new-wikilegis/admin/login/\?([^=\n]+)\=([^&\n]+)$',
         r'/admin/login/?next=\2'),
        (r'/new-wikilegis/admin/logout/?$', '/admin/logout'),
        (r'/new-wikilegis/login/?$', '/accounts/login'),
        (r'/new-wikilegis/login/\?([^=\n]+)\=([^&\n]+)$',
         r'/accounts/login/?next=\2'),
        (r'/new-wikilegis/logout/?$', '/accounts/logout'),
    )
