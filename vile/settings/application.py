#!/usr/bin/env python
# -*- coding: utf-8 -*-


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5pz)=n%7_q8xdjksrl4!3tqulwq@)qe^)4cvnue9r-ib7l93#)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Site ID
SITE_ID = 1

# Always with www
PREPEND_WWW = False

# Allowed hosts
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

# Custom applications
CUSTOM_APPS = [
    'vile',
    'person',
    'public',
    'feed'
]

# Middleware Classes
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'vile.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'vile.middleware.subdomain.SubdomainMiddleware',
    'vile.middleware.pagination.PaginationMiddleware',
]

# Base Url configuration
ROOT_URLCONF = 'vile.urls'

# WSGI Application
WSGI_APPLICATION = 'vile.wsgi.application'
