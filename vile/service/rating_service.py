# -*- coding: utf-8 -*-
from django.db import models


def rating_hash(instance):
    """
    Model related hash for votting
    :param instance:
    :return:
    """
    if not hasattr(instance, 'pk'):
        raise AttributeError('Instance has no attribute PK')
    return '{}:{}'.format(type(instance).__name__, instance.pk)


class Votable(object):
    """
    Votable model interface
    """
    def vote(self, author, positive=True):
        from vile.models import Vote
        vote = Vote.create(author=author, positive=positive, instance=self)
        vote.save()

        # Update karma
        if hasattr(self, 'karma') and hasattr(self, 'save'):
            self.karma = Vote.rating(self)
            self.save()
        return vote

    @property
    def rating(self):
        from vile.models import Vote
        return Vote.rating(self)
