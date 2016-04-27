# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from core.views import MassificadoPageListView
from .models import MassificadoUser
from .forms import EntrieUserForm


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
    template_name = 'page-entries-user.html'


class EntrieUserEditView(LoginRequiredMixin, UpdateView):
    model = MassificadoUser
    form_class = EntrieUserForm
    template_name = 'page-entries-user.html'

    def get_context_data(self, **kwargs):
        context = super(EntrieUserNewView, self).get_context_data(**kwargs)
        context['permission_groups'] = Group.objects.all()
        return context

    def get_success_url(self):
        pass


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
    context_object_name = 'profile'
    template_name = 'page-entries-profile.html'
    fields = ['name', 'permissions']

    def get_context_data(self, **kwargs):
        context = super(EntrieProfileEditView, self).get_context_data(**kwargs)
        # context += ENTRIES_PAGES
        context['entries_pages'] = ({
                'name': page[1],
                'can_view': '%s_can_view' % page[0],
                'can_edit': '%s_can_edit' % page[0],
        } for page in ENTRIES_PAGES )

        return context

    def get_success_url(self):
        return reverse_lazy('entries-profiles')