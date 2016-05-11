from __future__ import unicode_literals
from cleave.encrypt import Encrypt
from django.db import models
from django.templatetags.static import static
from feed.models import Hashtag
from person.models import Person
from vile.service import Votable
from django.conf import settings


class Public(models.Model, Votable):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    full_description = models.TextField(null=True, blank=True)
    slug = models.CharField(null=True, blank=True, max_length=24)
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

    @property
    def facility(self):
        # return Encrypt('club.{}'.format(self.pk)).md5[:8].lower()
        return 'public'

    @property
    def new_members(self):
        return self.members.order_by('-id')[:9]

    @property
    def recent_founders(self):
        return self.founders.order_by('-id')

    @property
    def image(self):
        if not self.avatar:
            return static('media/noavatar.jpg')
        return '/{}'.format(self.avatar.url)

    @property
    def slug_allowed(self):
        return self.members.all().count() > settings.SLUGABLE_CLUB_MEMEBERS

    @property
    def recent_entries(self):
        from feed.models import Entry
        return Entry.objects.filter(publisher=self).order_by('-id').all()[:50]

    def vote(self, author, positive=True):
        super(Public, self).vote(author, positive)
        for person in self.founders.all():
            person.vote(author=author, positive=positive)
        return self.owner.vote(author=author, positive=positive)