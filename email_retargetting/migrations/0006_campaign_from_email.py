# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-27 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_campaigns', '0005_email_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='from_email',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
