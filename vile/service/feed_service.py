#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from django.utils.timezone import now, timedelta
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from feed.models import Entry, Hashtag
from public.models import Public


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

    RELATED_TIMEDELTA = {
        'days': 7
    }

    @staticmethod
    def get_queryset(search_term=None, club=None):
        # Exclude private publications
        qs = Entry.objects.exclude(
            publisher__is_closed=True,
            publisher__is_public=False
        )

        # If club exists
        if club is not None and isinstance(club, Public):
            qs = qs.filter(publisher=club)

        # Get only new publications
        qs = qs.filter(created_at__gte=now() - timedelta(**RelatedFeeds.RELATED_TIMEDELTA))

        # Filter by query term
        if search_term:
            tags = Hashtag.get_or_create(search_term.split(','))
            qs = qs.filter(Q(tags__in=tags) | Q(publisher__tags__in=tags))

        # Return uniques ids
        return qs.values('id').distinct()

    @staticmethod
    def list(search_term=None, page=1, club=None):
        qs = RelatedFeeds.get_queryset(search_term=unicode(search_term), club=club)
        paginator = Paginator(qs, settings.PER_PAGE)

        if page > paginator.num_pages:
            return []

        cur_stack = paginator.page(page)
        RelatedFeeds.has_next_page = cur_stack.has_next()

        return Entry.objects.filter(
            id__in=map(lambda x: x['id'], cur_stack)
        ).order_by(*RelatedFeeds.ORDER_BY)

    has_next_page = False


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
    LINKS = re.compile(ur'((link|url)(["\'](.+?)["\'])*:(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+))\s')
    IMAGES = re.compile(ur'((image|img)(["\'](.+?)["\'])*:(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+))\s')
    YOUTUBE = re.compile(ur'((youtube|yt):(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+))\s')
    HASHTAGS = re.compile(ur'#([^\s]+)')

    def __init__(self, content='', max_length=255, max_lines=5):
        self.content = unicode(content + u' ')
        self.max_length = max_length
        self.max_lines = max_lines

    def __str__(self):
        return self.full()

    def short(self):
        out = u'\n'.join(self.content.split(u'\n')[:self.max_lines])
        out = out[:self.max_length]

        if len(out) < len(self.content):
            out += u'...'

        return ContentProcessor.compile(out)

    def full(self):
        return ContentProcessor.compile(self.content)

    @staticmethod
    def get_hashtags(text):
        text = unicode(text)
        return ContentProcessor.HASHTAGS.findall(text)

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
        return text.replace('<', u'&lt;').replace('>', u'&gt;')

    @staticmethod
    def _compile_lines(text, delimiter=u'<br>'):
        return text.replace('\n', delimiter)

    @staticmethod
    def _compile_links(text, links):
        out = text
        for link in links:
            src = link[0]
            url = link[4]
            title = link[3].strip() or url
            out = out.replace(src, u'<a href="{}" target="_blank">{}</a>'.format(url, title))

        return out

    @staticmethod
    def _compile_images(text, links):
        out = text
        for link in links:
            src = link[0]
            url = link[4]
            title = link[3].strip() or url
            out = out.replace(src, u'<a href="{}" target="_blank">'
                                   u'<img class="embed image" src="{}" alt="{}">'
                                   u'</a>'.format(url, url, title))

        return out

    @staticmethod
    def _compile_hashtags(text, tags):
        print tags, ' in ', text
        out = text
        for tag in tags:
            tag = unicode(tag)
            out = out.replace(u'#' + tag, u'<a href="?hash={}">{}</a>'.format(unicode(tag), u'#' + tag))

        return out

    @staticmethod
    def _compile_youtube(text, links):
        out = text
        for link in links:
            src = link[0]
            code = {x.split('=')[0]: x.split('=')[1] for x in link[2].split('?')[1].split('&')}.get('v')
            if code is None:
                continue

            out = out.replace(src, u'<iframe '
                                   u'class="embed video youtube" '
                                   u'src="https://www.youtube.com/embed/{}" '
                                   u'frameborder="0" allowfullscreen>'
                                   u'</iframe>'.format(unicode(code)))

        return out