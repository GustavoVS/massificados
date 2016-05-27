from django import forms
from .models import MassificadoGroups


class MassificadoGroupsEditForm(forms.ModelForm):
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
        )
