# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 03:38
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='storm',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='storm',
            name='path',
            field=django.contrib.gis.db.models.fields.LineStringField(default=None, null=True, srid=4326),
        ),
    ]