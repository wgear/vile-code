from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from vile.service import VotableModel


class Person(AbstractUser, VotableModel):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_index=True)
    verified = models.BooleanField(default=False, blank=True, db_index=True)
    register_date = models.DateTimeField(auto_created=True, blank=True, null=True)
