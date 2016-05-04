#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from feed.models import Entry, Hashtag


class RelatedFeeds(object):
    """
    Related fields service
    """
    ORDER_BY = [
        '-publisher__is_confirmed',
        '-karma',
        '-publisher__karma',
        '-id'
    ]

    @staticmethod
    def get_queryset(search_term=None):
        qs = Entry.objects.exclude(publisher__is_closed=True, publisher__is_public=False)
        if search_term:
            tags = Hashtag.get_or_create(search_term.split(','))
            qs = qs.filter(Q(tags__in=tags) | Q(publisher__tags__in=tags))

        return qs.order_by(*RelatedFeeds.ORDER_BY)

    @staticmethod
    def list(search_term=None, page=1):
        qs = RelatedFeeds.get_queryset(search_term=search_term)
        paginator = Paginator(qs, settings.PER_PAGE)
        if page > paginator.num_pages:
            return []

        return paginator.page(page)


class RelatedTags(object):
    """
    Related hashtags service
    """
    ORDER_BY = [
        '-karma',
        'name',
    ]

    @staticmethod
    def get_queryset(search_term):
        qs = Hashtag.objects
        if search_term:
           qs.filter(name__contains=search_term)

        return qs.order_by(*RelatedTags.ORDER_BY)

    @staticmethod
    def list(search_term, page=1):
        qs = RelatedTags.get_queryset(search_term=search_term)
        paginator = Paginator(qs, settings.PER_PAGE)
        if page > paginator.num_pages or page < 0 or not isinstance(page, int):
            return []

        return paginator.page(page)
