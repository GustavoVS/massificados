# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory

# from product.models import Question
from sale.models import Sale, Buyer, BuyerAddress, Deadline, File, Detail


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['name', 'phone', 'email', 'kind_person', 'cpf_cnpj', ]


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
        fields = ['begin', 'end', 'status', 'payment', 'proposal', 'policy', ]

DeadlineSaleFormset = inlineformset_factory(
    Sale, Deadline, form=DeadlineSaleForm, extra=0, min_num=1, can_delete=False)


class FileDeadlineForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['document', 'file_type']

FileDeadlineFormset = inlineformset_factory(
    Deadline, File, form=FileDeadlineForm, extra=1, min_num=0, can_delete=False)


class DetailDeadlineForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ['name']

    def __init__(self, question=None, *args, **kwargs):
        return super(DetailDeadlineForm, self).__init__(*args, **kwargs)

DetailDeadlineFormset = inlineformset_factory(
    Deadline, Detail, form=DetailDeadlineForm, extra=0, min_num=1, can_delete=False)
