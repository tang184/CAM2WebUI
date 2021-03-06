# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20170613_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membername', models.CharField(max_length=50, verbose_name='Member Name')),
                ('memberimg', models.CharField(blank=True, max_length=300, null=True, verbose_name='Member Image')),
                ('iscurrentmember', models.BooleanField(verbose_name='Is Current Member')),
            ],
        ),
        migrations.DeleteModel(
            name='CurrentMember',
        ),
        migrations.DeleteModel(
            name='OldMember',
        ),
    ]
