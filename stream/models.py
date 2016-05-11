from __future__ import unicode_literals
from django.db import models


class Message(models.Model):
    message = models.TextField()

    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class PublicMessage(Message):
    author = models.ForeignKey('person.Person', related_name='author')
    target = models.ForeignKey('public.Public', related_name='to_public')


class DialogueMessage(Message):
    author = models.ForeignKey('person.Person', related_name='from_user')
    target = models.ForeignKey('person.Person', related_name='to_user')
