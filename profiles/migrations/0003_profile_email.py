# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-04 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20180504_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(default='abcd@gmail.com', max_length=120),
            preserve_default=False,
        ),
    ]
