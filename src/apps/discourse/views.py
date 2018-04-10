from apps.core.views import EdemProxyView
from django.conf import settings


class DiscourseProxyView(EdemProxyView):
    upstream = settings.DISCOURSE_UPSTREAM
    diazo_theme_template = 'diazo-discourse.html'
