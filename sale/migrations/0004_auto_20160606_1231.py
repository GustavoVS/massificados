# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-06 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0003_auto_20160606_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deadline',
            name='payment',
            field=models.FloatField(blank=True, null=True, verbose_name='Debt'),
        ),
    ]
