# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import vile.service.rating_service


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('karma', models.IntegerField(default=0, db_index=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            bases=(models.Model, vile.service.rating_service.Votable),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('content', models.TextField()),
                ('karma', models.IntegerField(default=0, db_index=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            bases=(models.Model, vile.service.rating_service.Votable),
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, db_index=True)),
                ('karma', models.IntegerField(default=0, db_index=True, blank=True)),
            ],
            bases=(models.Model, vile.service.rating_service.Votable),
        ),
    ]
