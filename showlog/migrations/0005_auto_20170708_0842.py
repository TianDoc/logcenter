# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-08 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showlog', '0004_auto_20170707_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='showmessage',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='control',
            name='nokeyword',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
