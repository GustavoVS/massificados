# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from core.views import MassificadoPageListView
from .models import MassificadoUser


class EntriesUsersView(LoginRequiredMixin, MassificadoPageListView):
    context_object_name = 'cadastros'
    template_name = 'page-entries-users.html'
    def get_queryset(self):
        return MassificadoUser.objects.all()


class EntriesProfilesView(LoginRequiredMixin, MassificadoPageListView):
    context_object_name = 'cadastros'
    template_name = 'page-entries-profiles.html'

    def get_queryset(self):
        return Group.objects.all()
