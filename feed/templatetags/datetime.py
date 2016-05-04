#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.timezone import now
from django import template


register = template.Library()


@register.filter('dtf')
def date_time_format(datetime=None):
    datetime = datetime or now()

    return str(datetime)
