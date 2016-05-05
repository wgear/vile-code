#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import datetime, time
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
        qs = Entry.objects.exclude(
            publisher__is_closed=True,
            publisher__is_public=False,
            created_at__lt=datetime.datetime.now() - datetime.timedelta(days=1)
        )

        if search_term:
            tags = Hashtag.get_or_create(search_term.split(','))
            qs = qs.filter(Q(tags__in=tags) | Q(publisher__tags__in=tags))

        return qs.values('id').distinct()

    @staticmethod
    def list(search_term=None, page=1):
        qs = RelatedFeeds.get_queryset(search_term=search_term)
        paginator = Paginator(qs, settings.PER_PAGE)
        if page > paginator.num_pages:
            return []

        return Entry.objects.filter(
            id__in=map(lambda x: x['id'], paginator.page(page))
        ).order_by(*RelatedFeeds.ORDER_BY)


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


class ContentProcessor(object):
    LINKS = re.compile(r'((link|url)(["\'](.+?)["\'])*:(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+))\s')
    IMAGES = re.compile(r'((image|img)(["\'](.+?)["\'])*:(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+))\s')
    YOUTUBE = re.compile(r'((youtube|yt):(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+))\s')
    HASHTAGS = re.compile(r'#(\w+)')

    def __init__(self, content='', max_length=255, max_lines=5):
        self.content = content + ' '

    def __str__(self):
        return self.full()

    def short(self):
        out = '\n'.join(self.content.split('\n')[:5])
        out = out[:255]

        if len(out) < len(self.content):
            out += '...'

        return ContentProcessor.compile(out)

    def full(self):
        return ContentProcessor.compile(self.content)

    @staticmethod
    def compile(text):
        out = ContentProcessor._clear_tags(text)

        # Compile links
        links = ContentProcessor.LINKS.findall(out)
        out = ContentProcessor._compile_links(out, links)

        # Compile youtube
        youtube = ContentProcessor.YOUTUBE.findall(out)
        out = ContentProcessor._compile_youtube(out, youtube)

        # Compile images
        images = ContentProcessor.IMAGES.findall(out)
        out = ContentProcessor._compile_images(out, images)

        # Compile hashtags
        tags = ContentProcessor.HASHTAGS.findall(out)
        out = ContentProcessor._compile_hashtags(out, tags)

        # Compile newlines
        out = ContentProcessor._compile_lines(out)

        return out

    @staticmethod
    def _clear_tags(text):
        return text.replace('<', '&lt;').replace('>', '&gt;')

    @staticmethod
    def _compile_lines(text, delimiter='<br>'):
        return text.replace('\n', delimiter)

    @staticmethod
    def _compile_links(text, links):
        out = text
        for link in links:
            src = link[0]
            url = link[4]
            title = link[3].strip() or url
            out = out.replace(src, '<a href="{}" target="_blank">{}</a>'.format(url, title))

        return out

    @staticmethod
    def _compile_images(text, links):
        out = text
        for link in links:
            src = link[0]
            url = link[4]
            title = link[3].strip() or url
            out = out.replace(src, '<a href="{}" target="_blank">'
                                   '<img class="embed image" src="{}" alt="{}">'
                                   '</a>'.format(url, url, title))

        return out

    @staticmethod
    def _compile_hashtags(text, tags):
        out = text
        for tag in tags:
            out = out.replace('#' + tag, '<a href="/?hash={}">{}</a>'.format(tag, '#' + tag))

        return out

    @staticmethod
    def _compile_youtube(text, links):
        out = text
        for link in links:
            src = link[0]
            code = {x.split('=')[0]: x.split('=')[1] for x in link[2].split('?')[1].split('&')}.get('v')
            if code is None:
                continue

            out = out.replace(src, '<iframe '
                                   'class="embed video youtube" '
                                   'src="https://www.youtube.com/embed/{}" '
                                   'frameborder="0" allowfullscreen>'
                                   '</iframe>'.format(code))

        return out