# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0096_auto_20171123_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.ImageField(upload_to='profile_pics'),
        ),
    ]
