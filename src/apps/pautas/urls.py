from django.urls import re_path
from apps.pautas import views


urlpatterns = [
    re_path('(?P<path>.*)$', views.PautasProxyView.as_view()),
]
