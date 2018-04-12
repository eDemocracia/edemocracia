from django.urls import re_path
from apps.about import views


urlpatterns = [
    re_path('(?P<path>.*)$', views.AboutProxyView.as_view()),
]
