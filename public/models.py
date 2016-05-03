from __future__ import unicode_literals
from django.db import models
from feed.models import Hashtag
from person.models import Person
from vile.service import Votable
from django.conf import settings


class Public(models.Model, Votable):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    full_description = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to=settings.UPLOAD_AVATAR_DIR, null=True, blank=True)

    tags = models.ManyToManyField(Hashtag)
    owner = models.ForeignKey(Person)
    members = models.ManyToManyField(Person, related_name='members', blank=True)
    founders = models.ManyToManyField(Person, related_name='founders', blank=True)

    karma = models.IntegerField(db_index=True, default=0, blank=True)

    created_at = models.DateTimeField(auto_created=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    is_public = models.BooleanField(default=True, blank=True, db_index=True)
    is_indexed = models.BooleanField(default=True, blank=True, db_index=True)
    is_closed = models.BooleanField(default=False, blank=True, db_index=True)
    is_confirmed = models.BooleanField(default=False, blank=True, db_index=True)
