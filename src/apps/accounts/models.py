from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .choices import GENDER_CHOICES, UF_CHOICES


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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
