# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-11 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showlog', '0007_auto_20170710_0652'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='power',
            field=models.IntegerField(default=1),
        ),
    ]