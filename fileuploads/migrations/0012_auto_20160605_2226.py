# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160107235441 on 2016-06-05 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileuploads', '0011_auto_20160605_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='row',
            name='cut_off_number',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='row',
            name='result_number',
            field=models.FloatField(default=0),
        ),
    ]
