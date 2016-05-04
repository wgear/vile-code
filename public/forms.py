#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Public
from feed.models import Hashtag


class CreateClubForm(ModelForm):
    def __init__(self, owner=None, *args, **kwargs):
        data = kwargs.get('data')
        if owner is not None and data:
            data.setlist('tags', Hashtag.get_or_create(data.getlist('tags'), lambda x: x.pk))
            data.setlist('owner', [owner.pk])
            kwargs['data'] = data
        super(CreateClubForm, self).__init__(*args, **kwargs)

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
