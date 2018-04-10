from django.urls import re_path
from apps.discourse import views


urlpatterns = [
    re_path('(?P<path>.*)$', views.DiscourseProxyView.as_view()),
]
