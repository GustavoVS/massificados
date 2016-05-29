# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# from product.models import Product
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site


class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.FileField(null=True)
    date_create = models.DateTimeField(_('Date created'), default=timezone.now)
    email = models.EmailField()
    cnpj = models.CharField(max_length=18)
    site = models.OneToOneField(Site)
    internal_code = models.CharField(max_length=100, null=True)
    operational_code = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # if not self.site:
        #     s = Site(domain='slug', name=self.name)
        #     s.save()
        #     self.site = s

        return super(Partner, self).save(*args, **kwargs)


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE
    )
    # product = models.ForeignKey(
    #     Product,
    #     on_delete=models.CASCADE
    # )

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
