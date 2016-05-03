#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings


def data(request):
    return {
        'title': settings.RESOURCE_NAME
    }
