from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
import string
import random
from django.template.defaultfilters import slugify
from apps.accounts.storage import OverwriteStorage


def generate_username(email):
    if User.objects.filter(email=email).exists():
        return User.objects.get(email=email).username
    else:
        name = slugify(email.split('@')[0])[:29]
        if User.objects.filter(username=name).exists():
            return generate_username(
                name + random.choice(string.ascii_letters + string.digits))
        else:
            return name


class UserProfile(models.Model):
    gender = models.CharField(_('gender'), max_length=200, blank=True,
                              null=True)
    uf = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(_('country'), max_length=200, null=True,
                               blank=True)
    birthdate = models.DateField(_('birthdate'), blank=True, null=True)
    user = models.OneToOneField(User, related_name='profile',
                                on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True,
                               storage=OverwriteStorage())

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __unicode__(self):
        return '%s <%s>' % (self.user.get_full_name(), self.user.email)
