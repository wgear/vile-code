#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from feed.models import Comment


class CommentForm(ModelForm):
    def __init__(self, author=None, *args, **kwargs):
        data = kwargs.get('data')
        if author is not None and data:
            data.setlist('publisher', [author.pk])
            kwargs['data'] = data

        super(CommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = [
            'target',
            'content',
            'publisher'
        ]
