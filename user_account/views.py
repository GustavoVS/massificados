# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from core.views import MassificadoPageListView
from django.views.generic.edit import CreateView, UpdateView
from .models import MassificadoUser
from .forms import EntrieUserEditForm, EntrieUserNewForm


class EntriesUsersView(LoginRequiredMixin, MassificadoPageListView):
    context_object_name = 'users'
    template_name = 'page-entries-users.html'
    def get_queryset(self):
        return MassificadoUser.objects.all()


class EntriesProfilesView(LoginRequiredMixin, MassificadoPageListView):
    context_object_name = 'profiles'
    template_name = 'page-entries-profiles.html'

    def get_queryset(self):
        return Group.objects.all()


class EntrieUserNewView(LoginRequiredMixin, CreateView):
    form_class = EntrieUserNewForm
    template_name = 'page-entries-user.html'

    def get_success_url(self):
        return

class EntrieUserEditView(LoginRequiredMixin, UpdateView):
    form_class = EntrieUserEditForm
    template_name = 'page-entries-user.html'

    def get_success_url(self):
        return
