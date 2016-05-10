#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import translation
from django.conf import settings


class LocaleMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).
    """

    def process_request(self, request):
        language = request.user.language if not request.user.is_anonymous() else settings.DEFAULT_LANGUAGE
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()