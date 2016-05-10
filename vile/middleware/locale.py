#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import translation


class LocaleMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).
    """

    def process_request(self, request):
        translation.activate(request.user.language)
        request.LANGUAGE_CODE = translation.get_language()