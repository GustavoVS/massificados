from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from product.models import Product, Status, FileType


class AbstractMassificadoGroups(models.Model):
    name = models.CharField(_('Name'), max_length=100, blank=True)
    menu_products = models.BooleanField(_('Products'), default=False, blank=True)
    menu_dashboard = models.BooleanField(_('Dashboard'), default=False, blank=True)
    menu_production = models.BooleanField(_('Production'), default=False, blank=True)
    menu_entries = models.BooleanField(_('Entries'), default=False, blank=True)
    menu_entries_users = models.BooleanField(_('Users'), default=False, blank=True)
    menu_entries_profiles = models.BooleanField(_('Profiles'), default=False, blank=True)
    menu_entries_partners = models.BooleanField(_('Partners'), default=False, blank=True)
    menu_entries_products = models.BooleanField(_('Products'), default=False, blank=True)
    menu_notification = models.BooleanField(_('Notification'), default=False, blank=True)
    menu_profile = models.BooleanField(_('Profile'), default=False, blank=True)
    product = models.ManyToManyField(Product, blank=True)

    status_see = models.ManyToManyField(Status, related_name='user_status_see', blank=True)
    status_see_payment = models.ManyToManyField(Status, related_name='user_status_see_payment', blank=True)
    status_see_deadline = models.ManyToManyField(Status, related_name='user_status_see_deadline', blank=True)

    status_edit = models.ManyToManyField(Status, related_name='user_status_edit', blank=True)
    status_edit_payment = models.ManyToManyField(Status, related_name='user_status_edit_payment', blank=True)
    status_edit_deadline = models.ManyToManyField(Status, related_name='user_status_edit_deadline', blank=True)

    status_set = models.ManyToManyField(Status, related_name='user_status_set', blank=True)

    profiles = models.ManyToManyField('self', blank=True)
    filetype_see = models.ManyToManyField(FileType, related_name='user_filetype_see', blank=True)
    filetype_download = models.ManyToManyField(FileType, related_name='user_filetype_download', blank=True)

    class Meta:
        verbose_name_plural = _('Permissions')
        abstract = True

    def __unicode__(self):
        return self.name


class MassificadoGroups(AbstractMassificadoGroups):
    pass

