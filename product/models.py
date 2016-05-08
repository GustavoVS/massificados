# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField
from core.models import FileType
from core.models import Status
from django.utils.translation import ugettext_lazy as _


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=30)
    susep = models.CharField(max_length=12)

    def __unicode__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=30)
    code = models.IntegerField()

    def __unicode__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    KIND_PERSON_CHOICES = (
        ('F', _('Individual')),
        ('J', _('Legal Person')),
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    icon1 = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    icon2 = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    introduction = models.CharField(max_length=50)
    description = models.TextField()
    declaration = models.TextField()
    kind_person = models.CharField(max_length=1, choices=KIND_PERSON_CHOICES)
    insurance_company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    file_type = models.ManyToManyField(FileType)
    is_lead = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class MethodPayment(models.Model):
    name = models.CharField(max_length=15)
    product = models.ForeignKey(Product)
    bank = models.ForeignKey(Bank)

    def __unicode__(self):
        return self.name


class Domain(models.Model):
    name = models.CharField(max_length=100)
    result_value = models.CharField(max_length=100)
    domain_value = models.CharField(max_length=100)


class Question(models.Model):
    name = models.TextField()
    default = models.TextField()
    message = models.CharField(max_length=100)
    required = models.BooleanField()
    comment = models.BooleanField()
    TYPE_GROUP_CHOICES = (
        ('he', _('Header')),
        ('br', _('Broker')),    # Corretora
        ('cl', _('Client')),    # Cliente
        ('in', _('Insured')),   # Segurado
        ('co', _('Commercial Protection')),     # Coberturas que da home - para exibir
        ('pr', _('Profile Protection')),    # Coberturas do Perfil - para contratar
        ('te', _('tenant')),   # Locatário
        ('ps', _('Process')),   #Dados do processo
        ('le', _('Legal Opinion')), #Parecer Juridico
        ('ot', _('Other information')), #Outras informações
        ('ct', _('Collection')),    # Prêmio
        ('cd', _('Condition')),  # Condições do Produto
        ('fo', _('Footer')),
    )
    type_group = models.CharField(max_length=2, choices=TYPE_GROUP_CHOICES)
    TYPE_PROFILE_CHOICES = (
        ('pr', _('Profile Deadline')),
        ('pd', _('Profile Detail')),
    )
    type_profile = models.CharField(max_length=2, choices=TYPE_PROFILE_CHOICES)
    TYPE_DATA_CHOICES = (
        ('va', _('VarChar')),
        ('ch', _('CheckBox')),
        ('fl', _('Float')),
        ('li', _('Link')),
        ('ra', _('Range')),
        ('da', _('Date')),
        ('te', _('Text')),
        ('pe', _('Percent')),
    )
    type_data = models.CharField(max_length=2, choices=TYPE_DATA_CHOICES)
    mask = models.CharField(max_length=50)
    rule = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)
    is_printable = models.BooleanField(default=False)
    domain = models.ManyToManyField(Domain)
    # todo:domain_value e result_value domain = JSONField, type data, rule

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question)


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
