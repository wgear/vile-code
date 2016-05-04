from __future__ import unicode_literals
from django.db import models
from vile.service import Votable


class Hashtag(models.Model, Votable):
    name = models.CharField(max_length=32, db_index=True)
    karma = models.IntegerField(db_index=True, default=0, blank=True)

    def __unicode__(self):
        return '#{}'.format(self.name)

    @staticmethod
    def get_or_create(tags_list, filtering=None):
        print tags_list, 'sadasdasdasd'
        result = []
        for tag in tags_list:
            tag = tag.strip().lower()
            try:
                pk = int(tag)
                result.append(Hashtag.objects.get(pk=pk))
            except:
                if len(tag) < 2:
                    continue

                try:
                    instance = Hashtag.objects.get(name=tag)
                except Hashtag.DoesNotExist:
                    instance = Hashtag(name=tag)
                    instance.save()
                result.append(instance)
        return result if not filtering else map(filtering, result)


class Entry(models.Model, Votable):
    title = models.CharField(max_length=255)
    content = models.TextField()

    tags = models.ManyToManyField(Hashtag)
    publisher = models.ForeignKey('public.Public')

    karma = models.IntegerField(db_index=True, default=0, blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
