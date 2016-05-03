from __future__ import unicode_literals
from django.db import models
from vile.service import Votable


class Hashtag(models.Model, Votable):
    name = models.CharField(max_length=32, db_index=True)
    karma = models.IntegerField(db_index=True, default=0, blank=True)

    def __unicode__(self):
        return '#{}'.format(self.name)


class Entry(models.Model, Votable):
    title = models.CharField(max_length=255)
    content = models.TextField()

    tags = models.ManyToManyField(Hashtag)
    publisher = models.ForeignKey('public.Public')

    karma = models.IntegerField(db_index=True, default=0, blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
