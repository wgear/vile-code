# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-10 17:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import vile.service.rating_service


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Public',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('full_description', models.TextField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=24, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=b'static/uploads/avatar')),
                ('karma', models.IntegerField(blank=True, db_index=True, default=0)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_public', models.BooleanField(db_index=True, default=True)),
                ('is_indexed', models.BooleanField(db_index=True, default=True)),
                ('is_closed', models.BooleanField(db_index=True, default=False)),
                ('is_confirmed', models.BooleanField(db_index=True, default=False)),
                ('founders', models.ManyToManyField(blank=True, related_name='founders', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='feed.Hashtag')),
            ],
            bases=(models.Model, vile.service.rating_service.Votable),
        ),
    ]
