# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-11 10:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_auto_20171111_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='user',
        ),
    ]
