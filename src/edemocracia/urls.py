from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from apps.accounts.api import api_root, UserListAPI, get_participation_user
from apps.core.views import index
from apps.reports import urls as reports_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="eDemocracia API",
        default_version='v1',
        description="Portal criado para ampliar a participação social no \
                     processo legislativo e aproximar cidadãos e seus \
                     representantes por meio da interação digital.",
        contact=openapi.Contact(email="labhacker@camara.leg.br"),
        license=openapi.License(name="GNU General Public License v3.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('sobre/', include('apps.about.urls')),
    path('api/v1/', api_root),
    path('api/v1/user/', UserListAPI.as_view(), name='user_list_api'),
    path('api/v1/participation/<uuid:user>/', get_participation_user,
         name='participation_user_api'),
    path('reports/', include(reports_urls)),
]

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if settings.NEW_WIKILEGIS_ENABLED:
    urlpatterns.append(
        path('wikilegis/', include('apps.new_wikilegis.urls')))

if settings.WIKILEGIS_ENABLED:
    urlpatterns.append(path('wikilegis-arquivo/', include('apps.wikilegis.urls')))

if settings.PAUTAS_ENABLED:
    urlpatterns.append(path('pautaparticipativa/',
                            include('apps.pautas.urls')))

if settings.AUDIENCIAS_ENABLED:
    urlpatterns.append(path('audiencias/', include('apps.audiencias.urls')))


if settings.DISCOURSE_ENABLED:
    urlpatterns.append(path('expressao/', include('apps.discourse.urls')))

admin.site.site_header = 'e-Democracia'
