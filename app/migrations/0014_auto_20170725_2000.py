# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-25 20:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20170717_1927'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AppList',
            new_name='CAM2dbApi',
        ),
        migrations.RenameField(
            model_name='cam2dbapi',
            old_name='applist',
            new_name='appname',
        ),
    ]
