# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from partner.models import Partner
from user_groups.models import MassificadoGroups


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
    partner = models.ForeignKey(Partner, null=True, verbose_name=_("Partner"), related_name="Partner")
    director = models.ForeignKey('self', null=True, blank=True, verbose_name=_("Director"), related_name="user_director")
    master = models.ForeignKey('self', null=True, blank=True, verbose_name=_("Master"), related_name="user_master")
    agency = models.CharField(_('Agency'), max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True
        permissions = ()

    def __unicode__(self):
        return self.first_name or self.username or self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class MassificadoUser(AbstractMassificadoUser):
    group_permissions = models.ForeignKey(MassificadoGroups, null=True,
                                          verbose_name=_("Permissions"), related_name="Permissions")
