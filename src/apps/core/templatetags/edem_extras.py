from django import template
from django.template import defaultfilters

from apps.core import utils


register = template.Library()


@register.filter(name='str_to_date')
def str_to_date(value):
    return defaultfilters.date(utils.str_to_date(value),
                               "SHORT_DATE_FORMAT")
