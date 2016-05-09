# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory

from sale.models import Sale, Buyer, BuyerAddress, Deadline, Quote, File


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['name', 'email', 'cpf_cnpj',]


class BuyerAddressForm(forms.ModelForm):
    class Meta:
        model = BuyerAddress
        fields = ['street', 'district', 'complement', 'number', 'city', 'state', 'postal_code', ]

AddressBuyerFormset = inlineformset_factory(Buyer, BuyerAddress, form=BuyerAddressForm, extra=0, min_num=1)


class QuoteSaleForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['number', 'payment_date', 'value', 'maturity_date']

QuoteSaleFormset = inlineformset_factory(Deadline, Quote, form=QuoteSaleForm, extra=0, min_num=1)


class DeadlineSaleForm(forms.ModelForm):

    class Meta:
        model = Deadline
        fields = ['begin', 'end']

DeadlineSaleFormset = inlineformset_factory(Sale, Deadline, form=DeadlineSaleForm, extra=0, min_num=1)


class FileSaleForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['file', 'file_type']

FileSaleFormset = inlineformset_factory(Deadline, File, form=FileSaleForm, extra=0, min_num=1)
