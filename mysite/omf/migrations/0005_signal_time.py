# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 00:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omf', '0004_remove_signal_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='signal',
            name='time',
            field=models.TextField(default='1', max_length=200),
            preserve_default=False,
        ),
    ]
