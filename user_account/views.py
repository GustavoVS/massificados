# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from core.views import MassificadoPageListView
from .models import MassificadoUser
from .forms import EntrieUserForm, EntrieProfileEditForm


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


class EntriesUsersView(LoginRequiredMixin, MassificadoPageListView):
    context_object_name = 'users'
    template_name = 'page-entries-users.html'

    def get_queryset(self):
        return MassificadoUser.objects.all()


class EntrieUserNewView(LoginRequiredMixin, CreateView):
    model = MassificadoUser
    context_object_name = 'user_entrie'
    form_class = EntrieUserForm
    template_name = 'page-entries-user.html'

    def get_success_url(self):
        return reverse_lazy('entries-users')


class EntrieUserEditView(LoginRequiredMixin, UpdateView):
    model = MassificadoUser
    context_object_name = 'user_entrie'
    form_class = EntrieUserForm
    template_name = 'page-entries-user.html'

    def get_success_url(self):
        return reverse_lazy('entries-users')


class EntriesProfilesView(LoginRequiredMixin, MassificadoPageListView):
    context_object_name = 'profiles'
    template_name = 'page-entries-profiles.html'

    def get_queryset(self):
        return Group.objects.all()


class EntrieProfileNewView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'page-entries-profile.html'
    fields = ['name', 'permissions']

    def get_success_url(self):
        return reverse_lazy('entries-profiles')


class EntrieProfileEditView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = EntrieProfileEditForm
    context_object_name = 'profile'
    template_name = 'page-entries-profile.html'

    def get_success_url(self):
        return reverse_lazy('entries-profiles')
