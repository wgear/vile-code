#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vile.service import MyPublic


def mypublic(request):
    return {
        'my_clubs': MyPublic.list(request)
    }
