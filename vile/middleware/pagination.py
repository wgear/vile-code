#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PaginationMiddleware:
    """ Filter requested page for pagination """

    def process_request(self, request):
        current_page = request.GET.get('page', 1)
        try:
            current_page = int(current_page)
        except:
            current_page = 1

        if current_page < 1:
            current_page = 1

        request.current_page = current_page
