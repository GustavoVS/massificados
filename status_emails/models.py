from __future__ import unicode_literals

from django.db import models
from product.models import ActionStatus
from django.utils.translation import ugettext_lazy as _
from user_account.models import MassificadoUser


class ActionStatusEmails(models.Model):
    action_status = models.ForeignKey(ActionStatus, on_delete=models.CASCADE)
    ACTION_EMAIL_CHOICES = (
        ('buy', _('Buyer')),
        ('inc', _('Insurance Company')),
        ('own', _('Owner')),
        ('usr', _('Users')),
    )
    action_email = models.CharField(max_length=3, choices=ACTION_EMAIL_CHOICES)

    def save(self):
        if self.pk is not None:
            old = ActionStatusEmails.objects.get(pk=self.pk)
            if self.action_email != old.action_email and old.action_email == 'usr':
                self.action_status_email_users_set.clear()

        return super(ActionStatusEmails, self).save()

    def __unicode__(self):
        return '%s - %s' % (self.action_status, self.action_email)


class ActionStatusEmailsUsers(models.Model):
    action_status_email = models.ForeignKey(ActionStatusEmails, on_delete=models.CASCADE)
    user = models.ForeignKey(MassificadoUser, on_delete=models.CASCADE)
