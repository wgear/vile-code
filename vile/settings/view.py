#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.utils.translation import ugettext_lazy as _


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Rows per page
PER_PAGE = 10

# Templates settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'vile.contextprocessor.settings.data',
                'vile.contextprocessor.feed.related',
                'vile.contextprocessor.public.mypublic',
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/es/1.9/topics/i18n/translation/#how-django-discovers-language-preference
LANGUAGE_CODE = 'en-gb'

LOCALE_PATHS = (
    os.path.join(ROOT_DIR, 'locale'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_LANGUAGE = 'en'
LANGUAGES = [
    ('ua', _('Ukranian')),
    ('ru', _('Russian')),
    ('en', _('English'))
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(ROOT_DIR, 'static'),
)

# Upload avatars dir
UPLOAD_AVATAR_DIR = 'static/uploads/avatar'
