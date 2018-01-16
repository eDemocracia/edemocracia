from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.accounts.choices import GENDER_CHOICES, UF_CHOICES
import string
import random
from django.template.defaultfilters import slugify


def generate_username(email):
    if User.objects.filter(email=email).exists():
        return User.objects.get(email=email).username
    else:
        name = slugify(email.split('@')[0])[:29]
        if User.objects.filter(username=name).exists():
            return generate_username(
                name + random.choice(string.letters + string.digits))
        else:
            return name


class UserProfile(models.Model):
    gender = models.CharField("gênero", max_length=200, choices=GENDER_CHOICES,
                              blank=True, null=True)
    uf = models.CharField(max_length=2, choices=UF_CHOICES, null=True,
                          blank=True)
    country = models.CharField("país", max_length=200, null=True, blank=True)
    birthdate = models.DateField("data de nascimento", blank=True, null=True)
    user = models.OneToOneField(User, related_name='profile',
                                on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/")

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __unicode__(self):
        return '%s <%s>' % (self.user.get_full_name(), self.user.email)


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    instance.username = generate_username(instance.email)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
