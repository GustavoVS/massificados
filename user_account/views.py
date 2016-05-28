# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import  Q
from core.views import MassificadoPageListView
from user_groups.models import MassificadoGroups
from product.models import Product, Status, FileType
from .models import MassificadoUser
from .forms import EntrieUserForm
# from notifications.models import Notification


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

        if self.request.method == "GET":
            search = self.request.GET.get('search-input')
            if search:
                result = MassificadoUser.objects.filter(Q(email__contains=search) | Q(first_name__contains=search) | Q(last_name__contains=search))
            else:
                result = MassificadoUser.objects.all()
        else:
            result = MassificadoUser.objects.all()
        return result


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
        if self.request.method == "GET":
            search = self.request.GET.get('search-input')
            if search:
                result = MassificadoGroups.objects.filter(Q(name__contains=search))
            else:
                result = MassificadoGroups.objects.all()
        else:
            result = MassificadoUser.objects.all()
        return result


class NotificationsView(LoginRequiredMixin, ListView):
    template_name = 'page-notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        self.request.user.notifications.mark_all_as_read()
        return self.request.user.notifications.all()
