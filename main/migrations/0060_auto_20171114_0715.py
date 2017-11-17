# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 23:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0059_systemwallet_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemwallet',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
