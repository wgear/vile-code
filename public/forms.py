#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Public
from feed.models import Hashtag


class CreateClubForm(ModelForm):
    def __init__(self, owner, *args, **kwargs):
        self.owner = owner
        super(CreateClubForm, self).__init__(*args, **kwargs)

    def clean_owner(self):
        return self.owner.pk

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
            'tags',
        ]
