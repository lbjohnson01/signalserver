# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160107235441 on 2016-06-29 00:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileuploads', '0022_group_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='file_id',
            field=models.IntegerField(default=0),
        ),
    ]
