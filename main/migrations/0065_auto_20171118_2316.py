# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-18 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0064_auto_20171118_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='bookedDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='bookedEndTime',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='bookedStartTime',
            field=models.TimeField(null=True),
        ),
    ]