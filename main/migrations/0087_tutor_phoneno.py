# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 14:56
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0086_auto_20171122_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='phoneNo',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99999999)]),
        ),
    ]
