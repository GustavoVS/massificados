from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from product.models import Product, Status, FileTypeSee, FileTypeDownload


# class Profiles(models.Model):
#     name = models.CharField(max_length=100)

#     class Meta:
#         verbose_name_plural = _('Profiles')

#     def __unicode__(self):
#         return self.name


class AbstractMassificadoGroups(models.Model):
    name = models.CharField(_('First name'), max_length=100, blank=True)
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
    product = models.ManyToManyField(Product,)

    status_see = models.ManyToManyField(Status, related_name='user_status_see')
    status_edit = models.ManyToManyField(Status, related_name='user_status_edit')
    status_set = models.ManyToManyField(Status, related_name='user_status_set')

    profiles = models.ManyToManyField('self')
    filetype_see = models.ManyToManyField(FileTypeSee)
    filetype_download = models.ManyToManyField(FileTypeDownload)

    class Meta:
        verbose_name_plural = _('Permissions')
        abstract = True

    def __unicode__(self):
        return self.name


class MassificadoGroups(AbstractMassificadoGroups):
    pass
