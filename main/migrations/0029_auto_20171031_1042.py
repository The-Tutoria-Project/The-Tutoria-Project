# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 02:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_tutor_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='availability',
            options={'verbose_name_plural': 'Avaialabilities'},
        ),
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together=set([('tutor', 'weekday', 'startTime'), ('tutor', 'weekday', 'endTime'), ('tutor', 'weekday', 'startTime', 'endTime')]),
        ),
    ]
