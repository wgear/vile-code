#!/usr/bin/env python
# -*- coding: utf-8 -*-
from public.models import Public


class MyPublic(object):
    ORDER_BY = [
        'title',
        '-karma'
    ]

    @staticmethod
    def list(request):
        if not request.user.pk:
            return []

        return Public.objects\
            .filter(owner=request.user)\
            .order_by(*MyPublic.ORDER_BY)
