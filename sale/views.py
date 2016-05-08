# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from .models import Sale, Partner, Buyer, Status
from .forms import SaleBuyerFormSet, BuyerForm, FullSaleForm, AddressBuyerFormset
from product.models import Product


class SalesView(LoginRequiredMixin, ListView):
    model = Sale
    context_object_name = 'sales'
    template_name = 'page-sales.html'

    def get_queryset(self):
        return Sale.objects.all()


class CreateSaleView(LoginRequiredMixin, CreateView):
    model = Buyer
    form_class = BuyerForm
    template_name = 'page-sale.html'
    context_object = 'sale'

    def get_context_data(self, **kwargs):
        data = super(CreateSaleView, self).get_context_data(**kwargs)
        data['productpk'] = self.kwargs['productpk']
        data['addressbuyer'] = AddressBuyerFormset()
        return data

    def form_valid(self, form):
        response = super(CreateSaleView, self).form_valid(form)
        addresses = AddressBuyerFormset(self.request.POST)
        if addresses.is_valid():
            addresses.instance.buyer = self.object
            addresses.save()
        sale = Sale()
        sale.product = Product.objects.get(pk=self.request.POST['productpk'])
        sale.buyer = self.object
        sale.partner = Partner.objects.get(id=1)  # todo: Tirar esse hardcode do pértinêr
        sale.status = Status.objects.get(id=1)  # Status inicial
        sale.save()
        return response

    def get_success_url(self):
        return reverse_lazy('index_view')


class FullSaleView(LoginRequiredMixin, UpdateView):
    model = Sale
    form_class = FullSaleForm
    template_name = 'page-sale-full.html'

    def get_success_url(self):
        return reverse_lazy('')