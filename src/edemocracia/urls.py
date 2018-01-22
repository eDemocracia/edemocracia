from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from apps.accounts.api import api_root, UserListAPI


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('api/v1/', api_root),
    path('api/v1/user/', UserListAPI.as_view(), name='user_list_api'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.WIKILEGIS_ENABLED:
    urlpatterns.append(path('wikilegis/', include('apps.wikilegis.urls')))
