# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-23 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0002_trip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='enddate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='startdate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
