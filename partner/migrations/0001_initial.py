# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 07:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo', models.FileField(upload_to=b'')),
                ('slug', models.CharField(max_length=50)),
                ('date_create', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('modificate', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('cnpj', models.CharField(max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='Sac',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Partner')),
            ],
        ),
        migrations.CreateModel(
            name='SacItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('detail', models.TextField()),
                ('hour', models.CharField(max_length=100, null=True)),
                ('sac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Sac')),
            ],
        ),
        migrations.CreateModel(
            name='SacPhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=30)),
                ('sac_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.SacItem')),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Partner'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product'),
        ),
    ]