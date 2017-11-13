# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 19:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0055_sessions_sessionamount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('couponCode', models.CharField(default='000000', max_length=6)),
                ('expiryDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=6)),
                ('comments', models.CharField(max_length=256)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Student')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Tutor')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(default='HKD', max_length=3)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
