# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-10 06:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showlog', '0006_auto_20170708_1009'),
    ]

    operations = [
        migrations.DeleteModel(
            name='operate',
        ),
        migrations.AlterField(
            model_name='control',
            name='nokeyword',
            field=models.TextField(null=True),
        ),
    ]
