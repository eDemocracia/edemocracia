from apps.core.views import EdemProxyView
from django.conf import settings


class AudienciasProxyView(EdemProxyView):
    upstream = settings.AUDIENCIAS_UPSTREAM
    diazo_theme_template = 'diazo-base.html'
    rewrite = (
        (r'/audiencias/admin/login/?$', '/admin/login'),
        (r'/audiencias/admin/login/\?([^=\n]+)\=([^&\n]+)$',
         r'/admin/login/?next=\2'),
        (r'/audiencias/admin/logout/?$', '/admin/logout'),
        (r'/audiencias/login/?$', '/accounts/login'),
        (r'/audiencias/login/\?([^=\n]+)\=([^&\n]+)$',
         r'/accounts/login/?next=\2'),
        (r'/audiencias/logout/?$', '/accounts/logout'),
    )
