# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-26 01:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showlog', '0009_historytable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='control',
            name='nokeyword',
        ),
    ]