# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from product.models import Question, Product, Status, FileType
from partner.models import Partner
from user_account.models import MassificadoUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from core.notification import Notification


class Buyer(models.Model):
    KIND_PERSON_CHOICES = (
        ('F', _('Individual')),
        ('J', _('Legal Person')),
    )
    name = models.CharField(_('Name'), max_length=100)
    date_create = models.DateTimeField(_('Date created'), default=timezone.now)
    email = models.EmailField(_('E-mail'))
    phone = models.CharField(_('Phone'), max_length=14)
    kind_person = models.CharField(_('Kind Person'), max_length=1, choices=KIND_PERSON_CHOICES)
    cpf_cnpj = models.CharField(_('CPF/CNPJ'), max_length=18)

    def __unicode__(self):
        return self.name


class BuyerAddress(models.Model):
    buyer = models.ForeignKey(Buyer)
    street = models.CharField(_('Street'), max_length=100)
    district = models.CharField(_('District'), max_length=20)
    complement = models.CharField(_('Complement'), max_length=20, null=True, blank=True)
    number = models.CharField(_('Number'), max_length=6)
    city = models.CharField(_("City"), max_length=20)
    state = models.CharField(_("State"), max_length=20)
    postal_code = models.CharField(_('Postal Code'), max_length=9)
    is_main = models.BooleanField(_('Main Address'), default=True)

    def __unicode__(self):
        return self.street


class Sale(models.Model):
    create_timestamp = models.DateField(_('Date Created'), default=timezone.now())
    product = models.ForeignKey(Product)
    partner = models.ForeignKey(Partner)
    buyer = models.ForeignKey(Buyer)
    owner = models.ForeignKey(MassificadoUser)

    def __unicode__(self):
        return '%s (%s)' % (self.product, self.buyer)


class Deadline(models.Model):
    active = models.BooleanField(default=True)
    begin = models.DateField(_('Begin'))
    end = models.DateField(_('End'))
    status = models.ForeignKey(Status)
    payment = models.FloatField(_('Payment'))
    proposal = models.CharField(_('Proposal'), max_length=100)
    policy = models.CharField(_('Policy'), max_length=100)
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE
    )

    def get_questions(self):
        return self.sale.product.profile.questions_set.get(type_profile='pdl')

    def save(self, *a, **kw):
        if not self.status_id:
            self.status = self.sale.product.begin_status

        resp = super(Deadline, self).save(*a, **kw)

        if self.pk is None:
            status_emails = self.status.actionstatus_set.get(
                product=self.sale.product).actionstatusemails_set.all()
            if status_emails:
                recipients = ()
                for status_email in status_emails:
                    if status_email.action_email == 'own':
                        recipients += (self.sale.owner,)
                    elif status_email.action_email == 'buy':
                        recipients += (self.sale.buyer.email,)
                    elif status_email.action_email == 'inc':
                        recipients += (self.sale.product.insurance_company.email,)
                    elif status_email.action_email == 'usr':
                        for email_user in status_email.actionstatusemailsusers_set.all():
                            recipients += (email_user.user,)

                notification = Notification(actor=self, recipient=recipients)
                notification.send(
                    _('New Sale [%d] created') % (self.pk),
                    _('The Sale [%d] has status changed to %s . Buyer %s, CPF/CNPJ %s ') % (
                        self.pk, self.status, self.sale.buyer.name, self.sale.buyer.cpf_cnpj
                    )
                )
        else:
            new = Deadline.objects.get(pk=self.pk)
            if new.status != self.status:
                if new.status.actionstatus_set.filter(product=self.sale.product).exists():
                    status_emails = new.status.actionstatus_set.get(
                        product=self.sale.product).actionstatusemails_set.all()
                    if status_emails:
                        recipients = ()
                        for status_email in status_emails:
                            if status_email.action_email == 'own':
                                # recipients += (self.sale.product.owner, )
                                recipients += (self.sale.owner, )
                            elif status_email.action_email == 'buy':
                                recipients += (self.sale.buyer.email, )
                            elif status_email.action_email == 'inc':
                                recipients += (self.sale.product.insurance_company.email, )
                            elif status_email.action_email == 'usr':
                                for email_user in status_email.actionstatusemailsusers_set.all():
                                    recipients += (email_user.user, )

                        notification = Notification(actor=self, recipient=recipients)
                        notification.send(
                            _('Sale [%d] has status changed') % (self.pk),
                            _('The Sale [%d] has status changed from %s to %s . Buyer %s, CPF/CNPJ %s ') % (
                                self.pk, self.status, new.status, new.sale.buyer.name, new.sale.buyer.cpf_cnpj
                            )
                        )

        return resp


class File(models.Model):
    file_type = models.ForeignKey(FileType)
    deadline = models.ForeignKey(Deadline)
    document = models.FileField(_('Document'))

    def __unicode__(self):
        return self.file_type


class Quote(models.Model):
    number = models.IntegerField(_('Number'))
    value = models.FloatField(_('Value'))
    payment_date = models.DateField(_('Payment Date'))
    maturity_date = models.DateField(_('Maturity Date'))
    deadline = models.ForeignKey(Deadline)

    def __unicode__(self):
        return 'Quote %s' % self.number


class SubQuote(models.Model):
    number = models.IntegerField(_('Number'))
    value = models.FloatField(_('Value'))
    percentage = models.FloatField(_('Percentage'))
    payment_date = models.DateField(_('Payment Date'))
    maturity_date = models.DateField(_('Maturity Date'))
    deadline = models.ForeignKey(Deadline)
    quote = models.ForeignKey(Quote)
    user = models.ForeignKey(MassificadoUser)

    def __unicode__(self):
        return 'Sub Quote %d' % self.number


class Detail(models.Model):
    name = models.CharField(max_length=50)
    deadline = models.ForeignKey(
        Deadline,
        on_delete=models.CASCADE
    )

    def __unicode__(self):
        return self.name


class Response(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    value = models.TextField()

    class Meta:
        abstract = True


class ResponseDeadline(Response):
    deadline = models.ForeignKey(Deadline)

    def __unicode__(self):
        return '%s (%s - %s)' % (self.value, self.question, self.deadline)


class ResponseDetail(Response):
    detail = models.ForeignKey(Detail)
