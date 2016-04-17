# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from product.models import Product


class Partner(models.Model):
    name = models.CharField(max_length=100)
    galcorr_logo = models.CharField(max_length=80)
    parner_logo = models.CharField(max_length=80)
    url = models.CharField(max_length=250)
    create = models.DateField()
    modificate = models.DateField()
    email = models.EmailField()


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE
    )
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
    )

class Template():
    pass