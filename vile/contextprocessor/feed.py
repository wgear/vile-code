#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vile.service import RelatedTags


def related(request):
    return {
        'hot': RelatedTags.list('')
    }
