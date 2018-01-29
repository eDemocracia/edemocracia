from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from apps.accounts.api import api_root, UserListAPI
from django.views.generic import TemplateView
from apps.core.views import index

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('api/v1/', api_root),
    path('api/v1/user/', UserListAPI.as_view(), name='user_list_api'),
    path('form', TemplateView.as_view(template_name="form.html")),
    path('profile', TemplateView.as_view(template_name="profile.html")),
    path('404', TemplateView.as_view(template_name="404.html")),
    path('500', TemplateView.as_view(template_name="500.html")),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.WIKILEGIS_ENABLED:
    urlpatterns.append(path('wikilegis/', include('apps.wikilegis.urls')))

if settings.PAUTAS_ENABLED:
    urlpatterns.append(path('pautaparticipativa/',
                            include('apps.pautas.urls')))
