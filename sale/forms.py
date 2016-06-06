# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from pycpfcnpj import cpfcnpj
from sale.models import Sale, Buyer, BuyerAddress, Deadline, File, Detail, MethodPayment


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

    def clean_phone(self):
        if len(self.cleaned_data.get('phone')) < 14:
            raise forms.ValidationError(_('Invalid Phone Number'))

        return self.cleaned_data.get('phone')

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
    # accept_declaration = forms.BooleanField(_('I accept that the GalCorr make contact my client, if necessary'),
    #     required=True)
    payment = forms.CharField(max_length=18, required=False)

    class Meta:
        model = Deadline
        fields = ['begin', 'end', 'proposal', 'policy', 'accept_declaration', 'method_payment',
                  'insured_capital', 'rate_per_thousand', 'insured_group', 'costing', 'revenues', 'lives', 'payment']

    def __init__(self, *args, **kwargs):
        super(DeadlineSaleForm, self).__init__(*args, **kwargs)
        self.fields['method_payment'].initial = MethodPayment.objects.get(name='Boleto')
        if self.instance:
            self.fields['payment'].initial = self.instance.payment

    def clean_payment(self):
        payment = self.cleaned_data.get('payment')
        if payment:
            return float(self.cleaned_data.get('payment').replace('.', '').replace(',', '.'))
        else:
            return payment

    def clean_method_payment(self):
        return MethodPayment.objects.get(name='Boleto')
    # def clean_status(self):
    #     # todo:
    #     return self.cleaned_data.get('status')


DeadlineSaleFormset = inlineformset_factory(
    Sale, Deadline, form=DeadlineSaleForm, extra=0, min_num=1, can_delete=False)


class FileDeadlineInlineFormset(BaseInlineFormSet):

    def __init__(self, file_type, *args, **kwargs):
        super(FileDeadlineInlineFormset, self).__init__(*args, **kwargs)
        if file_type:
            for form in self.forms:
                form.fields['file_type'].queryset = file_type


class FileDeadlineForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['document', 'file_type']

FileDeadlineFormset = inlineformset_factory(
    Deadline, File, form=FileDeadlineForm, formset=FileDeadlineInlineFormset,
    extra=1, min_num=0, max_num=8, can_delete=False)


class DetailDeadlineForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ['name']

    def __init__(self, question=None, *args, **kwargs):
        return super(DetailDeadlineForm, self).__init__(*args, **kwargs)

DetailDeadlineFormset = inlineformset_factory(
    Deadline, Detail, form=DetailDeadlineForm, extra=0, min_num=1, can_delete=False)
