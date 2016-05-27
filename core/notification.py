from notifications.signals import notify
from django.core.mail import send_mail
from massificados.settings import NOTIFICATION_FROM_EMAIL
from django.utils.translation import ugettext_lazy as _
from user_account.models import MassificadoUser
from django.contrib.auth.models import Group


class Notification(object):
    recipient = actor = None

    def __init__(self, actor=None, recipient=None):
        self.actor = actor
        self.recipient = recipient

    def mail_notify(self, subject, message, from_email, recipient_list):
        send_mail(subject, message, from_email, recipient_list)

    def system_notification(self, actor, recipient, verb):
        notify.send(actor, recipient=recipient, verb=verb)

    def send(self, subject, message):

        if not self.actor:
            raise Exception(_('No object found to send the notification'))

        if not self.recipient:
            raise Exception(_('No recipients found to send the notification'))

        if self.recipient is MassificadoUser:
            mail_recipient = self.recipient.email
        elif self.recipient is Group:
            mail_recipient = ()
            for user in Group:
                mail_recipient += (user.email,)

        else:
            mail_recipient = self.recipient

        self.mail_notify(subject, message, NOTIFICATION_FROM_EMAIL, mail_recipient)
        self.system_notification(self.actor, self.recipient, message)
