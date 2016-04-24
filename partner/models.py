# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from product.models import Product
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.FileField()
    slug = models.CharField(max_length=50)
    date_create = models.DateTimeField(_('Date created'), default=timezone.now)
    modificate = models.DateField()
    email = models.EmailField()
    cnpj = models.CharField(max_length=18)

    def __unicode__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    def __unicode__(self):
        return self.name


class Sac(models.Model):
    name = models.CharField(max_length=100)
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE
    )

    def __unicode__(self):
        return self.name


class SacItem(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField()
    hour = models.CharField(max_length=100, null=True)
    sac = models.ForeignKey(
        Sac,
        on_delete=models.CASCADE
    )

    def __unicode__(self):
        return self.name


class SacPhone(models.Model):
    description = models.CharField(max_length=100)
    number = models.CharField(max_length=30)
    sac_item = models.ForeignKey(
        SacItem,
        on_delete=models.CASCADE
    )

    def __unicode__(self):
        return self.description

class Adress():
    pass


class SocialMedia():
    pass


class Template():
    pass
