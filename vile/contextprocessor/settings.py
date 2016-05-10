#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings


def data(request):
    return {
        'title': settings.RESOURCE_NAME,
        'allowed_langs': map(lambda x: x[0], settings.LANGUAGES)
    }
