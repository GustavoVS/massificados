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
        # import ipdb; ipdb.set_trace()
        mail_recipient = notify_recipient = ()
        if isinstance(self.recipient, MassificadoUser):
            mail_recipient = self.recipient.email
            notify_recipient = self.recipient
        elif isinstance(self.recipient, Group):
            notify_recipient = Group
            mail_recipient = ()
            for user in Group:
                mail_recipient += (user.email,)
        elif isinstance(self.recipient, tuple) or isinstance(self.recipient, list):
            for recipient in self.recipient:
                if isinstance(recipient, MassificadoUser):
                    mail_recipient += (recipient.email, )
                    self.system_notification(self.actor, recipient, message)
                else:
                    mail_recipient += (recipient, )

        self.mail_notify(subject, message, NOTIFICATION_FROM_EMAIL, mail_recipient)

        if notify_recipient:
            self.system_notification(self.actor, notify_recipient, message)
