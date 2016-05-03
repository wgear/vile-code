#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from vile.service import rating_hash


class Vote(models.Model):
    positive = models.BooleanField(default=True, blank=True, db_index=True)
    author = models.ForeignKey('person.Person', db_index=True)
    to = models.CharField(max_length=255, db_index=True)

    @staticmethod
    def rating(instance):
        return Vote.objects.filter(to=rating_hash(instance), positive=True).count() - \
               Vote.objects.filter(to=rating_hash(instance), positive=False).count()

    @staticmethod
    def create(author, instance, positive=True):
        exists = Vote.objects.filter(author=author, to=rating_hash(instance))
        if exists.count() > 0:
            exists = exists.first()
            exists.positive = positive
            return exists
        return Vote(positive=positive, to=rating_hash(instance), author=author)