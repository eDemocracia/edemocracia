from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from apps.accounts.models import UserProfile
from registration.views import RegistrationView as BaseRegistrationView
from registration.models import RegistrationProfile
from registration.users import UserModel
from registration import signals
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from apps.accounts import captcha
from django.views.generic import UpdateView
from django.contrib import messages
from apps.accounts.forms import UserProfileForm
from django.urls import reverse


class CustomRegistrationView(BaseRegistrationView):
    http_method_names = ['post']
    SEND_ACTIVATION_EMAIL = getattr(settings, 'SEND_ACTIVATION_EMAIL', True)
    success_url = 'registration_complete'
    template_name = 'registration/custom_registration_form.html'

    registration_profile = RegistrationProfile

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        captcha_response = captcha.verify(form.data['g-recaptcha-response'])
        if captcha_response['success']:
            response = super().form_valid(form)
            if self.request.is_ajax():
                data = {
                    'data': _("Please check your email to complete the"
                              " registration process."),
                }
                return JsonResponse(data, status=200)
            else:
                return response
        else:
            message = ' '.join(
                map(lambda x: captcha.ERRORS[x],
                    captcha_response['error-codes'])
            )
            data = {
                'data': message,
            }
            return JsonResponse(data, status=401)

    def register(self, form):
        site = get_current_site(self.request)

        if hasattr(form, 'save'):
            new_user_instance = form.save()
        else:
            new_user_instance = (UserModel().objects
                                 .create_user(**form.cleaned_data))

        profile = UserProfile.objects.get(user=new_user_instance)
        profile.uf = form.cleaned_data['uf']
        profile.country = form.cleaned_data['country']
        profile.birthdate = form.cleaned_data['birthdate']
        profile.gender = form.cleaned_data['gender']
        profile.save()

        new_user = self.registration_profile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=self.request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user

    def registration_allowed(self):
        return getattr(settings, 'REGISTRATION_OPEN', True)


@csrf_exempt
def ajax_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        response_data = {}
        if form.is_valid():
            login(request, form.get_user())
            status_code = 200
        else:
            response_data['data'] = _("Invalid user and/or password.")
            status_code = 401
        return JsonResponse(response_data, status=status_code)
    else:
        return HttpResponse(status=405)


class ProfileView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'registration/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        messages.success(self.request, 'Perfil modificado com sucesso!')
        return reverse('profile')
