from django.urls import re_path
from apps.wikilegis import views


urlpatterns = [
    re_path('(?P<path>.*)$', views.WikilegisProxyView.as_view()),
]
