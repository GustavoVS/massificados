# -*- coding: utf-8 -*-
from django.views.generic import ListView
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


class MassificadoPageListView(ListView):
    def get_context_data(self, *args, **kwargs):
        context = super(MassificadoPageListView, self).get_context_data(*args, **kwargs)
        return context


class IndexView(MassificadoPageListView):
    model = Product
    context_object_name = 'home_product'
    template_name = "index.html"

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['products_f'] = Product.objects.filter(kind_person='F')
        context['products_j'] = Product.objects.filter(kind_person='J')
        context['products'] = Product.objects.all()
        return context


class EntriesView(LoginRequiredMixin, MassificadoPageListView):
    context_object_name = 'cadastros'
    template_name = 'page-entries.html'

    def get_queryset(self):
        return self.request.user.user_permissions.all()
