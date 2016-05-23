# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from partner.models import Partner
from product.models import Product, StatusSee, StatusEdit, StatusSet, FileTypeSee, FileTypeDownload


class AbstractMassificadoUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_REGEXP = re.compile('^[\w.+-]+$')
    username = models.CharField(
        _('Username'), max_length=30, unique=True,
        help_text=_("Required. 30 characters or fewer. Letters, numbers and "
                    "./+/-/_ characters"),
        validators=[
            validators.RegexValidator(USERNAME_REGEXP, _('Enter a valid username.'), 'invalid')
        ])
    email = models.EmailField(_('Email address'), blank=False, unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)
    partner = models.ForeignKey(Partner, null=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True
        permissions = ()

    def __unicode__(self):
        return self.first_name or self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class Permissions(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Permissions'

    def __unicode__(self):
        return self.name


class MassificadoGroups(models.Model):
    name = models.CharField(max_length=100)
    menu_products = models.BooleanField(_('Products'), default=False)
    menu_dashboard = models.BooleanField(_('Dashboard'), default=False)
    menu_production = models.BooleanField(_('Production'), default=False)
    menu_entries = models.BooleanField(_('Entries'), default=False)
    menu_notification = models.BooleanField(_('Notification'), default=False)
    menu_profile = models.BooleanField(_('Profile'), default=False)
    product = models.ManyToManyField(Product, null=True, blank=True)
    status_see = models.ManyToManyField(StatusSee, null=True, blank=True)
    status_edit = models.ManyToManyField(StatusEdit, null=True, blank=True)
    status_set = models.ManyToManyField(StatusSet, null=True, blank=True)
    permissions = models.ManyToManyField(Permissions, null=True, blank=True)
    filetype_see = models.ManyToManyField(FileTypeSee, null=True, blank=True)
    filetype_download = models.ManyToManyField(FileTypeDownload, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Groups'

    def __unicode__(self):
        return self.name


class MassificadoUser(AbstractMassificadoUser):
    group_permissions = models.ForeignKey(MassificadoGroups, null=True)