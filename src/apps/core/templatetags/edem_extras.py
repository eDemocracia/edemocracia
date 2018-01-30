from django import template
from datetime import datetime
from django.template import defaultfilters

register = template.Library()


@register.filter(name='str_to_date')
def str_to_date(value):
    result_date = datetime.strptime(value, "%Y-%m-%d").date()
    return defaultfilters.date(result_date, "SHORT_DATE_FORMAT")
