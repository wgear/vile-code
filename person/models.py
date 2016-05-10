from __future__ import unicode_literals
from cleave.encrypt import Encrypt
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from vile.service import Votable
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _


class Person(AbstractUser, Votable):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_CHOICES = (
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female'))
    )

    karma = models.IntegerField(db_index=True, default=0, blank=True)
    avatar = models.ImageField(upload_to=settings.UPLOAD_AVATAR_DIR, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_index=True)

    friends = models.ManyToManyField('self', verbose_name='friends')
    guests = models.ManyToManyField('self', verbose_name='guests')
    language = models.CharField(choices=settings.LANGUAGES, max_length=5, default='ru', blank=True)

    confirmation = models.CharField(max_length=8, blank=True, null=True)
    verified = models.BooleanField(default=False, blank=True, db_index=True)
    register_date = models.DateTimeField(auto_created=True, blank=True, null=True)

    @property
    def new_friends(self):
        return self.friends.order_by('-id')[:9]

    @property
    def new_guests(self):
        return self.guests.order_by('-id')[:9]

    @property
    def publics(self):
        from public.models import Public
        return Public.objects.filter(owner=self)

    @property
    def followed(self):
        from public.models import Public
        return Public.objects.filter(members__in=[self])

    @property
    def image(self):
        if not self.avatar:
            return static('media/noavatar.jpg')
        return '/{}'.format(self.avatar.url)

    def save(self, *args, **kwargs):
        if not self.verified:
            self.confirmation = Encrypt(self.username).upper()[0:8]
        return super(Person, self).save(*args, **kwargs)

    def verify(self):
        self.verified = True
        self.confirmation = None
        return self.save()
