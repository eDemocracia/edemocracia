from django.urls import path, include
from apps.accounts.views import CustomRegistrationView, ajax_login, ProfileView
from django.contrib.auth.decorators import login_required
from django.conf import settings


urlpatterns = [
    path('', include('registration.backends.default.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('ajax/signup/', CustomRegistrationView.as_view(),
         name='registration_register'),
    path('ajax/login/', ajax_login, name="ajax_login"),
]

if not settings.CAMARA_LOGIN:
    urlpatterns.append(path('profile/', login_required(
                       ProfileView.as_view()), name='profile'),)
