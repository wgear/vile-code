# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-10 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='public',
            name='slug',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
    ]
