# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
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


class Profiles(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Profiles'

    def __unicode__(self):
        return self.name


class AbstractMassificadoGroups(models.Model):
    name = models.CharField(_('First name'), max_length=100, blank=True)
    menu_products = models.BooleanField(_('Products'), default=False)
    menu_dashboard = models.BooleanField(_('Dashboard'), default=False)
    menu_production = models.BooleanField(_('Production'), default=False)
    menu_entries = models.BooleanField(_('Entries'), default=False)
    menu_entries_users = models.BooleanField(_('Users'), default=False)
    menu_entries_profiles = models.BooleanField(_('Profiles'), default=False)
    menu_entries_partners = models.BooleanField(_('Partners'), default=False)
    menu_entries_products = models.BooleanField(_('Products'), default=False)
    menu_notification = models.BooleanField(_('Notification'), default=False)
    menu_profile = models.BooleanField(_('Profile'), default=False)
    product = models.ManyToManyField(Product,)
    status_see = models.ManyToManyField(StatusSee,)
    status_edit = models.ManyToManyField(StatusEdit,)
    status_set = models.ManyToManyField(StatusSet,)
    profiles = models.ManyToManyField(Profiles,)
    filetype_see = models.ManyToManyField(FileTypeSee,)
    filetype_download = models.ManyToManyField(FileTypeDownload,)

    class Meta:
        verbose_name_plural = 'Permissions'
        abstract = True

    def __unicode__(self):
        return self.name


class MassificadoGroups(AbstractMassificadoGroups):
    pass


class MassificadoUser(AbstractMassificadoUser):
    group_permissions = models.ForeignKey(MassificadoGroups, null=True)
