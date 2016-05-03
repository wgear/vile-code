from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from vile.service import Votable


class Person(AbstractUser, Votable):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    )

    karma = models.IntegerField(db_index=True, default=0, blank=True)
    avatar = models.ImageField(upload_to=settings.UPLOAD_AVATAR_DIR, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_index=True)
    verified = models.BooleanField(default=False, blank=True, db_index=True)
    register_date = models.DateTimeField(auto_created=True, blank=True, null=True)

    def verify(self):
        self.verified = True
        from public.models import Public
        return Public.objects.filter(owner=self).update(is_confirmed=True)
