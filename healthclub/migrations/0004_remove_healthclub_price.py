# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-06 01:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthclub', '0003_healthclub_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthclub',
            name='price',
        ),
    ]
