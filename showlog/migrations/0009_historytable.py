# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-26 01:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showlog', '0008_control_power'),
    ]

    operations = [
        migrations.CreateModel(
            name='historytable',
            fields=[
                ('date', models.TextField()),
                ('host', models.CharField(max_length=30)),
                ('time', models.IntegerField()),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
