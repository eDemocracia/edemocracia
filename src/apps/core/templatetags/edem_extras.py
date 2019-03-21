from django import template
from datetime import datetime
from django.template import defaultfilters


register = template.Library()


@register.filter(name='str_to_date')
def str_to_date(value):
    result_date = datetime.strptime(value.split('T')[0], "%Y-%m-%d").date()
    return defaultfilters.date(result_date, "SHORT_DATE_FORMAT")


@register.filter(name='is_closed')
def is_closed(value):
    if datetime.strptime(value, "%Y-%m-%d").date() < datetime.today().date():
        return True
    else:
        return False
