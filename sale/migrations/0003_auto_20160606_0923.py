# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-06 09:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0002_auto_20160605_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deadline',
            name='lives',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sale.NumberLives', verbose_name='Lives'),
        ),
        migrations.AlterField(
            model_name='deadline',
            name='method_payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.MethodPayment', verbose_name='Method'),
        ),
    ]
