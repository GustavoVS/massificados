# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from pycpfcnpj import cpfcnpj
from sale.models import Sale, Buyer, BuyerAddress, Deadline, File, Detail


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['name', 'phone', 'email', 'kind_person', 'cpf_cnpj', 'responsible', 'activity_area']

    def clean_cpf_cnpj(self):
        if not cpfcnpj.validate(self.cleaned_data.get('cpf_cnpj').replace('.', '').replace('/', '').replace('-', '')):
            raise forms.ValidationError(_('Invalid value for this Field'))
        return self.cleaned_data.get('cpf_cnpj')

    def clean_responsible(self):
        if self.cleaned_data.get('kind_person') == 'J':
            if not self.cleaned_data.get('responsible'):
                raise forms.ValidationError(_('This field is required'))

        return self.cleaned_data.get('responsible')

    def clean_activity_area(self):
        if self.cleaned_data.get('kind_person') == 'J':
            if not self.cleaned_data.get('activity_area'):
                raise forms.ValidationError(_('This field is required'))

        return self.cleaned_data.get('activity_area')


class BuyerAddressForm(forms.ModelForm):
    class Meta:
        model = BuyerAddress
        fields = ['street', 'district', 'complement',
                  'number', 'city', 'state', 'postal_code', ]

AddressBuyerFormset = inlineformset_factory(Buyer, BuyerAddress, form=BuyerAddressForm, extra=0, min_num=1,
                                            can_delete=False)


class DeadlineSaleForm(forms.ModelForm):
    class Meta:
        model = Deadline
        fields = ['begin', 'end', 'payment', 'proposal', 'policy', 'accept_declaration', 'method_payment']

    # def clean_status(self):
    #     # todo:
    #     return self.cleaned_data.get('status')


DeadlineSaleFormset = inlineformset_factory(
    Sale, Deadline, form=DeadlineSaleForm, extra=0, min_num=1, can_delete=False)


class FileDeadlineForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['document', 'file_type']

FileDeadlineFormset = inlineformset_factory(
    Deadline, File, form=FileDeadlineForm, extra=0, min_num=0, max_num=8, can_delete=False)


class DetailDeadlineForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ['name']

    def __init__(self, question=None, *args, **kwargs):
        return super(DetailDeadlineForm, self).__init__(*args, **kwargs)

DetailDeadlineFormset = inlineformset_factory(
    Deadline, Detail, form=DetailDeadlineForm, extra=0, min_num=1, can_delete=False)
