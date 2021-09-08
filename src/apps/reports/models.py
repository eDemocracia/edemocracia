from django.db import models
from django.utils.translation import ugettext_lazy as _


PERIOD_CHOICES = (
    ('daily', _('Daily')),
    ('monthly', _('Monthly')),
    ('yearly', _('Yearly')),
    ('all', _('All the time')),
)

class NewUsersReport(models.Model):
    created = models.DateTimeField(_('created'), editable=False,
                                   blank=True, auto_now_add=True)
    modified = models.DateTimeField(_('modified'), editable=False,
                                    blank=True, auto_now=True)
    start_date = models.DateField(_('start date'), db_index=True)
    end_date = models.DateField(_('end date'), db_index=True)
    period = models.CharField(_('period'), max_length=200, db_index=True,
                              choices=PERIOD_CHOICES, default='daily')
    new_users = models.IntegerField(_('new users'), null=True, blank=True,
                                    default=0)
    class Meta:
        verbose_name = _('new user')
        verbose_name_plural = _('new users')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)
