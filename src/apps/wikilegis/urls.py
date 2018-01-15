from django.urls import path
from apps.wikilegis import views


urlpatterns = [
    path('<path:path>', views.WikilegisProxyView.as_view()),
]
