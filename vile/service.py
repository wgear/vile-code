# -*- coding: utf-8 -*-
from django.db import models


class VotableModel(object):
    positive = models.ManyToManyField('person.Person', related_name='positive')
    negative = models.ManyToManyField('person.Person', related_name='negative')
    cached_rating = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=1.0)

    @property
    def rating(self):
        return float(self.positive.count() - self.negative.count()) / 100

    def rating_changed(self, prev, new):
        self.cached_rating = new
        return self.save()

    def add_vote(self, user):
        prev = self.rating
        self.positive.remove(user)
        self.negative.remove(user)
        self.positive.add(user)
        self.save()

        return self.rating_changed(prev=prev, new=self.rating) if prev != self.rating else True

    def sub_vote(self, user):
        prev = self.rating
        self.positive.remove(user)
        self.negative.remove(user)
        self.negative.add(user)
        self.save()

        return self.rating_changed(prev=prev, new=self.rating) if prev != self.rating else True