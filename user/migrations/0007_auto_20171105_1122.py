# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20171105_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='abstract',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
