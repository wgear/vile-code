#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Public
from feed.models import Hashtag


class CreateClubForm(ModelForm):
    class Meta:
        model = Public
        fields = [
            'title',
            'description',
            'full_description',
            'avatar',
            'is_public',
            'is_indexed',
            'owner',
            'tags'
        ]
