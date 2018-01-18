from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class SignUpAjaxForm(forms.ModelForm):
    uf = forms.CharField(required=False)
    country = forms.CharField(required=False)
    birthdate = forms.DateField(required=False)
    gender = forms.CharField(required=False)

    required = ('email', 'password', 'first_name')

    error_messages = {
        'empty_email': _('This field is required.'),
        'exists_email': _('There is already a user registered with'
                          ' this email.'),
        'length_password': _('The password must be at least 6'
                             ' characters long.'),
        'empty_uf_country': _('The state or country fields must be filled in.'),
        'empty_uf': _('Select a UF, if you are a foreigner, '
                      'click on I am a foreigner'),
        'empty_country': _('Select a country, if you are not a foreigner,'
                           ' click on "I am Brazilian".'),
    }

    class Meta:
        fields = ('email', 'password', 'first_name')
        model = User

    def clean(self):
        cleaned_data = super(SignUpAjaxForm, self).clean()
        uf = cleaned_data.get("uf", None)
        country = cleaned_data.get("country", None)

        if not uf and not country:
            self.add_error('uf', mark_safe(
                self.error_messages.get('empty_uf')))
            self.add_error('country', mark_safe(
                self.error_messages.get('empty_country')))
            raise forms.ValidationError(mark_safe(
                self.error_messages.get('empty_uf_country')))

        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get("password", None)

        if len(password) < 6:
            raise forms.ValidationError(
                mark_safe(self.error_messages.get('length_password')))

        return password

    def clean_email(self):
        email = self.cleaned_data.get("email", None)
        users = User.objects.filter(email=email)

        if not email:
            raise forms.ValidationError(
                mark_safe(self.error_messages.get('empty_email')))

        if users.exists():
            raise forms.ValidationError(
                mark_safe(self.error_messages.get('exists_email')))

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
