# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField
from core.models import Status, FileType
from product.models import Question, Product
from partner.models import Partner
from user_account.models import MassificadoUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Buyer(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    date_create = models.DateTimeField(_('Date created'), default=timezone.now)
    email = models.EmailField(_('E-mail'))
    cpf_cnpj = models.CharField(_('CPF/CNPJ'), max_length=18)

    def __unicode__(self):
        return self.name


class BuyerAddress(models.Model):
    buyer = models.ForeignKey(Buyer)
    street = models.CharField(_('Street'), max_length=100)
    district = models.CharField(_('District'), max_length=20)
    complement = models.CharField(_('Complement'), max_length=20, null=True)
    number = models.CharField(_('Number'), max_length=6)
    city = models.CharField(_("City"), max_length=20)
    state = models.CharField(_("State"), max_length=20)
    postal_code = models.CharField(_('Postal Code'), max_length=9)
    is_main = models.BooleanField(_('Main Address'))

    def __unicode__(self):
        return self.street


class Sale(models.Model):
    create_timestamp = models.DateField(_('Date Created'), default=timezone.now())
    product = models.ForeignKey(Product)
    partner = models.ForeignKey(Partner)
    buyer = models.ForeignKey(Buyer)
    status = models.ForeignKey(Status)

    def __unicode__(self):
        return '%s (%s)' % (self.product, self.buyer)


class File(models.Model):
    file_type = models.ForeignKey(FileType)
    sale = models.ForeignKey(Sale)
    file = models.FileField(_('File'))

    def __unicode__(self):
        return self.file_type


class Quote(models.Model):
    number = models.IntegerField(_('Number'))
    value = models.FloatField(_('Value'))
    payment_date = models.DateField(_('Payment Date'))
    maturity_date = models.DateField(_('Maturity Date'))
    sale = models.ForeignKey(Sale)

    def __unicode__(self):
        return 'Quote %s' % self.number


class SubQuote(models.Model):
    number = models.IntegerField(_('Number'))
    value = models.FloatField(_('Value'))
    percentage = models.FloatField(_('Percentage'))
    payment_date = models.DateField(_('Payment Date'))
    maturity_date = models.DateField(_('Maturity Date'))
    sale = models.ForeignKey(Sale)
    quote = models.ForeignKey(Quote)
    user = models.ForeignKey(MassificadoUser)

    def __unicode__(self):
        return 'Sub Quote %d' % self.number


class Deadline(models.Model):
    begin = models.DateField(_('Begin'))
    end = models.DateField(_('End'))
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE
    )


class Detail(models.Model):
    deadline = models.ForeignKey(
        Deadline,
        on_delete=models.CASCADE
    )


class Response(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    question_value = JSONField
    result_value = JSONField
    detail = models.ForeignKey(Detail)
