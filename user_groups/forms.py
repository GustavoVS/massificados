from django import forms
from product.models import Product
from .models import MassificadoGroups


class MassificadoGroupsEditForm(forms.ModelForm):

    product_j = forms.ModelMultipleChoiceField(Product.objects.filter(kind_person='J'), required=False)
    product_f = forms.ModelMultipleChoiceField(Product.objects.filter(kind_person='F'), required=False)

    class Meta:
        model = MassificadoGroups
        fields = (
            'name',
            'menu_products',
            'menu_dashboard',
            'menu_production',
            'menu_entries',
            'menu_entries_users',
            'menu_entries_profiles',
            'menu_entries_partners',
            'menu_entries_products',
            'menu_notification',
            'menu_profile',
            'quote_see',
            'product',
            'status_see',
            'status_see_payment',
            'status_see_deadline',
            'status_edit',
            'status_edit_payment',
            'status_edit_deadline',
            'status_set',
            'profiles',
            'filetype_see',
            'filetype_download',
        )
