#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG = True

PREPEND_WWW = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vile',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '123'
    }
}
