# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-10 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20180510_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='document',
            field=models.FileField(upload_to='document'),
        ),
    ]
