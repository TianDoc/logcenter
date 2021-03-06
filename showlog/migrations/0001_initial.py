# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 11:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='control',
            fields=[
                ('keyword', models.CharField(max_length=30)),
                ('times', models.IntegerField()),
                ('contactsid', models.IntegerField()),
                ('contactsname', models.CharField(max_length=30)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='group',
            fields=[
                ('groupname', models.CharField(max_length=30)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='table',
            fields=[
                ('date', models.TextField()),
                ('name', models.CharField(max_length=30)),
                ('question', models.CharField(max_length=30)),
                ('host', models.CharField(max_length=30)),
                ('time', models.DateTimeField()),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('user', models.CharField(max_length=30)),
                ('telephone', models.CharField(max_length=30)),
                ('emailaddress', models.CharField(max_length=30)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('groupid', models.IntegerField()),
            ],
        ),
    ]
