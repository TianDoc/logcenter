# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-07 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showlog', '0002_user_groupname'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='nokeyword',
            field=models.CharField(max_length=90, null=True),
        ),
        migrations.AlterField(
            model_name='control',
            name='keyword',
            field=models.CharField(max_length=90),
        ),
    ]
