# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160107235441 on 2016-03-20 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileuploads', '0002_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='videofile',
            field=models.FileField(upload_to='/'),
        ),
    ]
