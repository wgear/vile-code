# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import vile.service.rating_service


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Public',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(null=True, auto_created=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('full_description', models.TextField(null=True, blank=True)),
                ('avatar', models.ImageField(null=True, upload_to=b'static/uploads/avatar', blank=True)),
                ('karma', models.IntegerField(default=0, db_index=True, blank=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_public', models.BooleanField(default=True, db_index=True)),
                ('is_indexed', models.BooleanField(default=True, db_index=True)),
                ('is_closed', models.BooleanField(default=False, db_index=True)),
                ('is_confirmed', models.BooleanField(default=False, db_index=True)),
                ('founders', models.ManyToManyField(related_name='founders', to=settings.AUTH_USER_MODEL, blank=True)),
                ('members', models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='feed.Hashtag')),
            ],
            bases=(models.Model, vile.service.rating_service.Votable),
        ),
    ]
