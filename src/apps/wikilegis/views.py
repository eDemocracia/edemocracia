from revproxy.views import DiazoProxyView
from django.conf import settings
import json


class WikilegisProxyView(DiazoProxyView):
    upstream = settings.WIKILEGIS_UPSTREAM
    diazo_theme_template = 'diazo-base.html'
    html5 = True

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        if request.user.is_authenticated:
            user_data = {
                'name': request.user.first_name,
                'email': request.user.email,
            }

            request.META['HTTP_REMOTE_USER_DATA'] = json.dumps(user_data)
            request.META['HTTP_AUTH_USER'] = request.user.username

        return super(WikilegisProxyView, self).dispatch(
            request, *args, **kwargs
        )
