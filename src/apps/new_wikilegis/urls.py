from django.urls import re_path
from apps.new_wikilegis import views


urlpatterns = [
    re_path('(?P<path>.*)$', views.NewWikilegisProxyView.as_view()),
]
