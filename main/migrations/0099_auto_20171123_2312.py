# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0098_auto_20171123_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.ImageField(blank=True, default='default_avatar.jpg', upload_to='profile_pics'),
        ),
    ]
