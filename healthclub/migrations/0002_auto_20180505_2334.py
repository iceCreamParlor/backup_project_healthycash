# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-05 23:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthclub', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='healthclub',
            old_name='price',
            new_name='price1',
        ),
        migrations.AddField(
            model_name='healthclub',
            name='price12',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='healthclub',
            name='price2',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='healthclub',
            name='price3',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='healthclub',
            name='price6',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]