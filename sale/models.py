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
    name = models.CharField(max_length=100)
    date_create = models.DateTimeField(_('Date created'), default=timezone.now)
    email = models.EmailField()
    cnpj = models.CharField(max_length=18)


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


class Sale(models.Model):
    create_timestamp = models.DateField(default=timezone.now())
    product = models.ForeignKey(Product)
    partner = models.ForeignKey(Partner)
    buyer = models.ForeignKey(Buyer)
    status = models.ForeignKey(Status)


class File(models.Model):
    file_type = models.ForeignKey(FileType)
    sale = models.ForeignKey(Sale)
    file = models.FileField()


class Quote(models.Model):
    number = models.IntegerField()
    value = models.FloatField()
    payment_date = models.DateField()
    maturity_date = models.DateField()
    sale = models.ForeignKey(Sale)


class SubQuote(models.Model):
    number = models.IntegerField()
    value = models.FloatField()
    percentage = models.FloatField()
    payment_date = models.DateField()
    maturity_date = models.DateField()
    sale = models.ForeignKey(Sale)
    quote = models.ForeignKey(Quote)
    user = models.ForeignKey(MassificadoUser)


class Deadline(models.Model):
    begin = models.DateField()
    end = models.DateField()
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

    class Meta:
        abstract = True


class ResponseDeadLine(Response):
    deadline = models.ForeignKey(Deadline)


class ResponseDatail(Response):
    detail = models.ForeignKey(Detail)



