from django.urls import re_path
from apps.audiencias import views


urlpatterns = [
    re_path('(?P<path>.*)$', views.AudienciasProxyView.as_view()),
]
