# -*- coding: utf-8 -*-
from django.views.generic import ListView
from product.models import Product
from user_account.models import MassificadoUser
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin


class MassificadoPageListView(ListView):
    def get_context_data(self, *args, **kwargs):
        context = super(MassificadoPageListView, self).get_context_data(*args, **kwargs)
        return context


class IndexView(MassificadoPageListView):
    context_object_name = 'home_product'
    template_name = "index.html"
    def get_queryset(self):
        return Product.objects.filter(kind_person='F')


class EntriesView(LoginRequiredMixin, MassificadoPageListView):
    context_object_name = 'cadastros'
    template_name = 'page-entries.html'

    def get_queryset(self):
        return self.request.user.user_permissions.all()
