from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from vile.service import VotableModel


class Hashtag(VotableModel, models.Model):
    name = models.CharField(max_length=32, db_index=True)

    def __unicode__(self):
        return '#{}'.format(self.name)


class Entry(models.Model, VotableModel):
    title = models.CharField(max_length=255)
    content = models.TextField()

    tags = models.ManyToManyField(Hashtag)
    publisher = models.ForeignKey('public.Public')

    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def rating_changed(self, prev, new):
        prev = self.publisher.cached_rating
        super(Entry, self).rating_changed(prev, new)

        self.publisher.rating_changed(prev, self.publisher.rating)

