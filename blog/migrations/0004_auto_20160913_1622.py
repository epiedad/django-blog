# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-13 16:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160913_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 13, 16, 22, 46, 716415, tzinfo=utc)),
        ),
    ]
