# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission

from product.models import Status

User = get_user_model()
# todo: compartilhar essa lista com o views.py
ENTRIES_PAGES = [
    ('user', _('Users')),
    ('profile', _('Users Profile')),
    ('product', _('Products')),
    ('partner', _('Partners')),
    ('campaign', _('Campaign')),
    ('sac', _('Sac')),
    ('dashboard', _('DashBoard')),
    ('report', _('Production Reports')),
]


class EntrieUserForm(forms.ModelForm):
    # is_staff = forms.BooleanField(required=False)
    # is_active = forms.BooleanField(required=False)

    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"), required=False)

    groups = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'partner')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        if self.cleaned_data['password1']:
            self.instance.set_password(self.cleaned_data['password1'])
        r = super(EntrieUserForm, self).save(commit=commit)
        self.instance.groups.clear()
        self.instance.groups.add(self.cleaned_data['groups'])
        return r


class EntrieProfileEditForm(forms.ModelForm):
    entries = []
    status = []

    # entries = forms.MultipleChoiceField(
    #             label='Entries',
    #             choices=[(c.id, c.name)
    #                 for c in Permission.objects.filter(
    #                     name__icontains='sac'
    #                 )
    #             ]
    # )

    # status = forms.MultipleChoiceField(label='Status', choices=[(m.id, m.name)
    #                       for m in Permission.objects.filter(name__icontains='status')
    #                   ])

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def save(self, commit=True):
        # for v in self.cleaned_data['entries']:

        # self.Group.permissions = self.cleaned_data['permissions_entries']

        return super(EntrieProfileEditForm, self).save(commit=commit)