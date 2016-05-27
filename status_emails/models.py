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

    def __unicode__(self):
        return 'Type "%s", Status "%s"' % (self.action_email, self.action_status)

    def save(self):
        if self.pk is not None:
            old = ActionStatusEmails.objects.get(pk=self.pk)
            if self.action_email != old.action_email and old.action_email == 'usr':
                self.action_status_email_users_set.clear()

        return super(ActionStatusEmails, self).save()


class ActionStatusEmailsUsers(models.Model):
    action_status_email = models.ForeignKey(ActionStatusEmails, on_delete=models.CASCADE)
    user = models.ForeignKey(MassificadoUser, on_delete=models.CASCADE)

    def __unicode__(self):
        return 'Action Status Email "%s", User "%s"' % (self.action_status_email, self.user)
