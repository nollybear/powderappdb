# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 23:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powderApp', '0002_remove_user_birthday'),
    ]

    operations = [
        migrations.CreateModel(
            name='PowderRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('altitudeDrop', models.CharField(max_length=5)),
                ('distance', models.CharField(max_length=5)),
                ('topSpeed', models.CharField(max_length=5)),
                ('avgSpeed', models.CharField(max_length=5)),
                ('biffsCount', models.CharField(max_length=5)),
                ('jumpsCount', models.CharField(max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]