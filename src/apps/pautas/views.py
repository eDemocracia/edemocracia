from apps.core.views import EdemProxyView
from django.conf import settings


class PautasProxyView(EdemProxyView):
    upstream = settings.PAUTAS_UPSTREAM
    diazo_theme_template = 'components/diazo-base.html'
    rewrite = (
        (r'/pautaparticipativa/admin/login/?$', '/admin/login'),
        (r'/pautaparticipativa/admin/login/\?([^=\n]+)\=([^&\n]+)$',
         r'/admin/login/?next=\2'),
        (r'/pautaparticipativa/admin/logout/?$', '/admin/logout'),
        (r'/pautaparticipativa/login/?$', '/accounts/login'),
        (r'/pautaparticipativa/login/\?([^=\n]+)\=([^&\n]+)$',
         r'/accounts/login/?next=\2'),
        (r'/pautaparticipativa/logout/?$', '/accounts/logout'),
    )
