# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_remove_availability_isavailable'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='isAvailable',
            field=models.BooleanField(default=True),
        ),
    ]