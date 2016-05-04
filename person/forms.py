#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from person.models import Person


class UpdateAvatarForm(ModelForm):
    def __init__(self, target=None, *args, **kwargs):
        super(UpdateAvatarForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Person
        fields = ['avatar']
