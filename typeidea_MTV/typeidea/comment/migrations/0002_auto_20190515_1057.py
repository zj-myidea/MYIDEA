# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-15 02:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.AddField(
            model_name='comment',
            name='target',
            field=models.CharField(default=1, max_length=500, verbose_name='评论目标'),
            preserve_default=False,
        ),
    ]