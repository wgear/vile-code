from __future__ import unicode_literals
import re
from django.db import models
from vile.service import Votable


class Hashtag(models.Model, Votable):
    name = models.CharField(max_length=32, db_index=True)
    karma = models.IntegerField(db_index=True, default=0, blank=True)

    def __unicode__(self):
        return '#{}'.format(self.name.replace(' ', ''))

    @staticmethod
    def get_or_create(tags_list, filtering=None):
        result = []
        for tag in tags_list:
            tag = unicode(tag.strip().lower().replace(' ', ''))
            try:
                pk = int(tag)
                result.append(Hashtag.objects.get(pk=pk))
            except:
                if len(tag) < 2:
                    continue

                instances = Hashtag.objects.filter(name=tag)
                if instances.count() > 0:
                    for tag in instances:
                        result.append(tag)
                else:
                    tag = Hashtag(name=tag)
                    tag.save()
                    result.append(tag)
        return result if not filtering else map(filtering, result)


class Entry(models.Model, Votable):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()

    tags = models.ManyToManyField(Hashtag)
    owner = models.ForeignKey('person.Person')
    publisher = models.ForeignKey('public.Public')

    karma = models.IntegerField(db_index=True, default=0, blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def comments(self):
        return Comment.objects.filter(target=self).order_by('-id')

    @property
    def comments_count(self):
        return Comment.objects.filter(target=self).count()

    def vote(self, author, positive=True):
        super(Entry, self).vote(author, positive)
        for tag in self.tags.all():
            tag.vote(author=author, positive=positive)
            tag.save()

        return self.publisher.vote(author=author, positive=positive)


class Comment(models.Model, Votable):
    target = models.ForeignKey(Entry)

    content = models.TextField()
    publisher = models.ForeignKey('person.Person')

    karma = models.IntegerField(db_index=True, default=0, blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
