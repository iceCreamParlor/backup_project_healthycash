# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-04 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthclub', '0003_remove_healthclub_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthclub',
            name='master',
        ),
        migrations.AddField(
            model_name='healthclub',
            name='member',
            field=models.IntegerField(default=0),
        ),
    ]
