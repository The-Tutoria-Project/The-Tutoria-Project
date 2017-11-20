# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 16:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0073_auto_20171121_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='sessions',
            unique_together=set([('studentID', 'tutorID', 'bookedDate'), ('studentID', 'tutorID', 'bookedDate', 'bookedStartTime', 'bookedEndTime')]),
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
    ]