#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from django import forms
from person.models import Person
from django.utils.translation import ugettext as _


class UpdateAvatarForm(forms.ModelForm):
    def __init__(self, target=None, *args, **kwargs):
        super(UpdateAvatarForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Person
        fields = ['avatar']


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=64, required=True)
    last_name = forms.CharField(max_length=64, required=True)
    username = forms.CharField(max_length=24, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        uname = self.data['username'].strip()
        if len(uname) > 24:
            raise forms.ValidationError(_('Username is too long. Please choose username between 4 and 24 characters'))

        if re.match(ur'/[^A-Z0-9\_А-Я]/', uname, re.IGNORECASE):
            raise forms.ValidationError(_('Username contains illegal characters. Only A-Z, 0-9 and _ are allowed'))

        if Person.objects.filter(username=uname).count() > 0:
            raise forms.ValidationError(_('Username already used by another user'))

        return uname

    def clean_password(self):
        if self.data['password'] != self.data['password1']:
            raise forms.ValidationError(_('Passwords does not match'))

        return self.data['password']

    def save(self):
        data = self.cleaned_data
        person = Person(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email']
        )

        person.set_password(data['password'])
        person.save()
        return person