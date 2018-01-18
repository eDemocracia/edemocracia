from django.urls import path, include
from apps.accounts.views import CustomRegistrationView, ajax_login


urlpatterns = [
    path('', include('registration.backends.default.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('ajax/signup/', CustomRegistrationView.as_view(), name='signup'),
    path('ajax/login/', ajax_login, name="ajax_login"),
]
