#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import safe
from vile.service import ContentProcessor


register = template.Library()


@register.filter('content')
def content_filter(value, full=None):
    """
    Filtering content and display tags
    :param value:
    :return:
    """
    value = ContentProcessor(value)
    try:
        return safe(value.full() if full else value.short())
    except:
        return ContentProcessor._clear_tags(value)