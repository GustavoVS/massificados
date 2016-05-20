# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-20 01:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('date_create', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('phone', models.CharField(max_length=14, verbose_name='Phone')),
                ('kind_person', models.CharField(choices=[('F', 'Individual'), ('J', 'Legal Person')], max_length=1, verbose_name='Kind Person')),
                ('cpf_cnpj', models.CharField(max_length=18, verbose_name='CPF/CNPJ')),
            ],
        ),
        migrations.CreateModel(
            name='BuyerAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=100, verbose_name='Street')),
                ('district', models.CharField(max_length=20, verbose_name='District')),
                ('complement', models.CharField(max_length=20, null=True, verbose_name='Complement')),
                ('number', models.CharField(max_length=6, verbose_name='Number')),
                ('city', models.CharField(max_length=20, verbose_name='City')),
                ('state', models.CharField(max_length=20, verbose_name='State')),
                ('postal_code', models.CharField(max_length=9, verbose_name='Postal Code')),
                ('is_main', models.BooleanField(default=True, verbose_name='Main Address')),
            ],
        ),
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('begin', models.DateField(verbose_name='Begin')),
                ('end', models.DateField(verbose_name='End')),
                ('payment', models.FloatField(verbose_name='Payment')),
                ('detail_count', models.IntegerField(verbose_name='Detail Count')),
                ('proposal', models.CharField(max_length=100, verbose_name='Proposal')),
                ('policy', models.CharField(max_length=100, verbose_name='Policy')),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to=b'', verbose_name='Document')),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Number')),
                ('value', models.FloatField(verbose_name='Value')),
                ('payment_date', models.DateField(verbose_name='Payment Date')),
                ('maturity_date', models.DateField(verbose_name='Maturity Date')),
            ],
        ),
        migrations.CreateModel(
            name='ResponseDeadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResponseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateField(default=datetime.datetime(2016, 5, 20, 1, 9, 3, 791000, tzinfo=utc), verbose_name='Date Created')),
            ],
        ),
        migrations.CreateModel(
            name='SubQuote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Number')),
                ('value', models.FloatField(verbose_name='Value')),
                ('percentage', models.FloatField(verbose_name='Percentage')),
                ('payment_date', models.DateField(verbose_name='Payment Date')),
                ('maturity_date', models.DateField(verbose_name='Maturity Date')),
                ('deadline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.Deadline')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.Quote')),
            ],
        ),
    ]
