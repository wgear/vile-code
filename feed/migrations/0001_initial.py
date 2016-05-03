# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 22:52
from __future__ import unicode_literals

from django.db import migrations, models
import vile.service


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            bases=(models.Model, vile.service.VotableModel),
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32)),
            ],
            bases=(vile.service.VotableModel, models.Model),
        ),
    ]
