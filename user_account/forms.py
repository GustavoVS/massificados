# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group


User = get_user_model()


class BaseUserEditForm(forms.ModelForm):
    email = forms.RegexField(label=_("email"), max_length=75, regex=r"^[\w.@+-]+$")
    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"), required=False)
    groups = forms.ModelMultipleChoiceField(Group.objects.none(), widget=forms.CheckboxSelectMultiple)
    model = User

    class Meta:
        model = User
        fields = []

    def clean_username(self):
        return self.instance.username

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
        return super(ProfileEditForm, self).save(commit=commit)

    def __init__(self, pass_a_Q_object=None, *args, **kwargs):
        super(BaseUserEditForm, self).__init__(*args, **kwargs)
        if pass_a_Q_object:
            self.fields['permissions'].queryset = Group.objects.filter(pass_a_Q_object)


class EntrieUserForm(BaseUserEditForm):
    fields = ('first_name', 'last_name', 'groups')
    def save(self, commit=True):
        pass