from django import forms
from django.forms.models import inlineformset_factory

from sale.models import Sale, Buyer, BuyerAddress


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = []

    def clean_product(self):
        return self.instance.product

    def clean_partner(self):
        return self.instance.partner


class FullSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = []


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['name', 'email', 'cnpj',]


class BuyerAddressForm(forms.ModelForm):
    class Meta:
        model = BuyerAddress
        fields = ['street', 'district', 'complement', 'number', 'city', 'state', 'postal_code', 'is_main', ]

AddressBuyerFormset = inlineformset_factory(Buyer, BuyerAddress, form=BuyerAddressForm, extra=1)
SaleBuyerFormSet = inlineformset_factory(Buyer, Sale, form=SaleForm, extra=1)
