from __future__ import unicode_literals
from django.db import models
from django.db.models import Sum
from feed.models import Hashtag
from person.models import Person
from vile.service import VotableModel


class Public(models.Model, VotableModel):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    full_description = models.TextField(null=True, blank=True)

    tags = models.ManyToManyField(Hashtag)
    members = models.ManyToManyField(Person, related_name='members')
    founders = models.ManyToManyField(Person, related_name='founders')

    created_at = models.DateTimeField(auto_created=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    is_public = models.BooleanField(default=True, blank=True, db_index=True)
    is_indexed = models.BooleanField(default=True, blank=True, db_index=True)
    is_closed = models.BooleanField(default=False, blank=True, db_index=True)
    is_confirmed = models.BooleanField(default=False, blank=True, db_index=True)

    @property
    def rating(self):
        public_votes = super(Public, self).rating
        feed_votes = self.feed_set.aggregate(total=Sum('float', 'cached_rating'))['total']
        members_votes = self.members.aggregate(total=Sum('float', 'cached_rating'))['total']
        confirm_bonus = 10 if self.is_confirmed else 0
        return sum([
            public_votes,
            feed_votes,
            members_votes,
            confirm_bonus
        ])
