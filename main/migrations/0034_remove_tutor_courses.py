# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 09:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_tutor_courses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='courses',
        ),
    ]
