# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-14 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_campaigns', '0010_auto_20170614_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='body',
            field=models.TextField(max_length=80000, verbose_name='Email body'),
        ),
    ]
