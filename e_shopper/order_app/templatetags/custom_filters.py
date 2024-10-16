import datetime
from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def add_days(value, days):
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value + timedelta(days=days)
    return value
