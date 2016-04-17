# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=30)
    susep = models.CharField(max_length=12)

class Bank(models.Model):
    name = models.CharField(max_length=30)
    code = models.IntegerField()

# Eu só precisava de uma classe, mas o Tony Ramos
class Branch(models.Model):
    name = models.CharField(max_length=50)


class FileType(models.Model):
    name = models.CharField(max_length = 20)


class Product(models.Model):
    KIND_PERSON_CHOICES = (
        ('F', _('Individual')),
        ('J', _('Legal Person')),
    )
    name = models.CharField(max_length=100)
    image = models.FileField()
    description = models.TextField()
    declaration = models.TextField()
    kind_person = models.CharField(max_length=1, choices=KIND_PERSON_CHOICES)
    insurance_company = models.ForeignKey(InsuranceCompany)
    branch = models.ForeignKey(Branch)
    file_type = models.ForeignKey(FileType)

class MethodPayment(models.Model):
    name = models.CharField(max_length=15)
    product = models.ForeignKey(Product)
    bank = models.ForeignKey(Bank)


class Question(models.Model):
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    required = models.BooleanField()
    TYPE_CHOICES = (
        ('pt', _('Protection')),
        ('co', _('Condition')),
        ('pr', _('Profile')),
        ('pd', _('Profile Detail')),
        ('sl', _('Sale')),
        ('in', _('Information')),
        ('dl', _('Deadline')),
    )
    type = models.CharField(max_length=1, choices= TYPE_CHOICES)
    domain = JSONField
    # domain_value e result_value


class Profile(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question)


class Status(models.Model):
    name = models.CharField(max_length=100)


class ActionStatus(models.Model):
    product = models.ForeignKey(Product)
    status = models.ForeignKey(Status)


class ActionStatusEmails(models.Model):
    ACTION_EMAIL_CHOICES = (
        ('buy', _('Buyer')),
        ('inc', _('Insurance Company')),
        ('psi', _('Partner - Superintendent')),
        ('pad', _('Partner - Administrator')),
        ('gop', _('GalCorr - Operational')),
        ('gco', _('GalCorr - Commercial')),
        ('gma', _('GalCorr - Manager')),
        ('gad', _('GalCorr - Administrator')),
    )
    action_email = models.CharField(max_length=3, choices=ACTION_EMAIL_CHOICES)
    action_status = models.ForeignKey(ActionStatus)
