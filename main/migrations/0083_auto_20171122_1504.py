# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 07:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0082_auto_20171122_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='session',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Sessions'),
        ),
    ]
