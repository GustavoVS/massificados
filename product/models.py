# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from user_account.models import MassificadoUser


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=30)
    susep = models.CharField(max_length=12)
    email = models.EmailField(_('Email address'), blank=True)

    def __unicode__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=80)
    code = models.IntegerField()

    def __unicode__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class FileType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class FileTypeSee(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.namema


class FileTypeDownload(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Status'

    def __unicode__(self):
        return self.name

    # def save(self):
    #
    #     return super(Status, self).save()


class StatusPermission(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'StatusPermissions'

    def __unicode__(self):
        return self.name


class StatusSee(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'StatusSee'

    def __unicode__(self):
        return self.name


class StatusEdit(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'StatusEdit'

    def __unicode__(self):
        return self.name


class StatusSet(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'StatusSet'

    def __unicode__(self):
        return self.name


class Product(models.Model):
    KIND_PERSON_CHOICES = (
        ('F', _('Individual')),
        ('J', _('Legal Person')),
    )
    name = models.CharField(_('Name'), max_length=100)
    image = models.ImageField(_('Image'), upload_to='uploads/%Y/%m/%d/', blank=True)
    icon1 = models.ImageField(_('Icon 1'), upload_to='uploads/%Y/%m/%d/', blank=True)
    icon2 = models.ImageField(_('Icon 2'), upload_to='uploads/%Y/%m/%d/', blank=True)
    introduction = models.CharField(_('Introduction'), max_length=50)
    description = models.TextField(_('Description'))
    declaration = models.TextField(_('Declaration'), blank=True)
    kind_person = models.CharField(max_length=1, choices=KIND_PERSON_CHOICES)
    insurance_company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    file_type = models.ManyToManyField(FileType)
    status_permission = models.ManyToManyField(StatusPermission)
    is_lead = models.BooleanField(default=False)
    begin_status = models.ForeignKey(Status)
    profile = models.ForeignKey(Profile, null=True)

    def __unicode__(self):
        return self.name


class MethodPayment(models.Model):
    name = models.CharField(_('Name'), max_length=15)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    hint = models.CharField(_('Hint'), max_length=100, blank=True)

    TYPE_GROUP_CHOICES = (
        ('hea', _('Header')),
        ('bro', _('Broker')),                       # Corretora
        ('cli', _('Client')),                       # Cliente
        ('ins', _('Insured')),                      # Segurado
        ('com', _('Commercial Protection')),        # Coberturas que da home - para exibir
        ('pro', _('Profile Protection')),           # Coberturas do Perfil - para contratar
        ('ten', _('Tenant')),                       # Locatário
        ('pss', _('Process')),                      # Dados do processo
        ('leg', _('Legal Opinion')),                # Parecer Juridico
        ('oth', _('Other information')),            # Outras informações
        ('col', _('Collection')),                   # Prêmio
        ('cdn', _('Condition')),                    # Condições do Produto
        ('foo', _('Footer')),
    )
    type_group = models.CharField(max_length=3, choices=TYPE_GROUP_CHOICES)
    TYPE_PROFILE_CHOICES = (
        ('pdl', _('Profile Deadline')),
        ('pdt', _('Profile Detail')),
    )
    type_profile = models.CharField(max_length=3, choices=TYPE_PROFILE_CHOICES)
    TYPE_DATA_CHOICES = (
        ('input', _('Input')),
        ('checkbox', _('CheckBox')),
        ('float', _('Float')),
        ('link', _('Link')),
        ('select', _('Select')),
        ('date', _('Date')),
        ('text', _('Text')),
        ('percent', _('Percent')),
        ('number', _('Number')),
    )
    type_data = models.CharField(max_length=10, choices=TYPE_DATA_CHOICES)
    rule = models.CharField(max_length=100, blank=True)
    is_default = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    is_printable = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)
    is_comment = models.BooleanField(default=False)
    default_value = models.CharField(max_length=100, blank=True)
    order_number = models.IntegerField(null=True, blank=True)
    col_width = models.IntegerField(null=True, blank=True)
    profile = models.ForeignKey(Profile)

    def __unicode__(self):
        type_profile_desc = ''
        for choice in self.TYPE_PROFILE_CHOICES:
            if choice[0] == self.type_profile:
                type_profile_desc = choice[1]
                break
        return '%s (%s)' % (self.name, type_profile_desc)


class Domain(models.Model):
    name = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name


class ActionStatus(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s (%s)' % (self.product, self.status)
