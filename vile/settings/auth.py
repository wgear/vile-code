#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Authentication
AUTH_USER_MODEL = 'person.Person'

# Authentication validations
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Django auth settings
LOGIN_URL = '/person/login/'
LOGIN_REDIRECT_URL = '/me'
