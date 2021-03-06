# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160107235441 on 2017-01-06 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0012_output_user_name'),
        ('groups', '0005_auto_20161209_2103'),
        ('fileuploads', '0035_video_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='outputs',
            field=models.ManyToManyField(to='signals.Output'),
        ),
        migrations.AddField(
            model_name='video',
            name='results',
            field=models.ManyToManyField(to='groups.Result'),
        ),
    ]
