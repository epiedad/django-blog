# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-13 16:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20160913_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
