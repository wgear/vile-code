#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Email configuration
# https://docs.djangoproject.com/ja/1.9/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_PASSWORD = '****'

EMAIL_HOST_USER = 'example@gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True