# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class BaseUserEditForm(forms.ModelForm):
    email = forms.RegexField(label=_("email"), max_length=75, regex=r"^[\w.@+-]+$")
    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"), required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name',)

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


class EntrieUserEditForm(BaseUserEditForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', )

    def save(self, commit=True):
        return super(BaseUserEditForm, self).save(commit=commit)


class EntrieUserNewForm(BaseUserEditForm):

    def save(self, commit=True):
        return super(BaseUserEditForm, self).save(commit=commit)
