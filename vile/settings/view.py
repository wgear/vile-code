#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

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
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(ROOT_DIR, 'static'),
)

# Upload avatars dir
UPLOAD_AVATAR_DIR = 'static/uploads/avatar'
