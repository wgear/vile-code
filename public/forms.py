#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import Public
from feed.models import Hashtag
from django.forms import ModelForm
from django.core.urlresolvers import reverse


class CreateClubForm(ModelForm):
    def __init__(self, owner=None, *args, **kwargs):
        data = kwargs.get('data')
        if owner is not None and data:
            data.setlist('tags', Hashtag.get_or_create(data.getlist('tags'), lambda x: x.pk))
            data.setlist('owner', [owner.pk])
            kwargs['data'] = data
        super(CreateClubForm, self).__init__(*args, **kwargs)

        self.fields['tags'].widget.attrs['class'] = 'tokenize'
        self.fields['tags'].widget.attrs['data-src'] = reverse('feed:hashtags')
        self.fields['tags'].widget.attrs['data-max'] = '8'

    class Meta:
        model = Public
        fields = [
            'title',
            'description',
            'full_description',
            'is_public',
            'is_indexed',
            'owner',
            'tags',
        ]
