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
    # formsets = [SaleBuyerFormSet, AddressBuyerFormset,]
    # formsets = [AddressBuyerFormset,]
    product = ''

    def get_context_data(self, **kwargs):
        data = super(CreateSaleView, self).get_context_data(**kwargs)
        self.product = Product.objects.get(pk=self.kwargs['productpk'])
        # for i, form in enumerate(self.formsets):
        #     data['f%d' % i] = form()
        data['addressbuyer'] = AddressBuyerFormset()
        return data

    def form_valid(self, form):
        form.save()
        f = AddressBuyerFormset(self.request.POST)
        if f.is_valid():
            f.instance.buyer = self.model
            f.save()

        sale = Sale()
        sale.product = self.product
        sale.buyer = self.model
        # todo: Tirar esse hardcode do partner
        sale.partner = Partner.objects.get(id=1)
        # Status inicial
        sale.status = Status.objects.get(id=1)
        sale.save()
        # self.model.product = self.product
        # for form in self.formsets:
        #     f = form(self.request.POST)
        #     if f.is_valid():
        #         f.instance.buyer = self.model
        #         # f.instance = self.object
        #         f.save()

        return super(CreateSaleView, self).form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(CreateSaleView, self).get_context_data(**kwargs)
    #     context['product'] = Product.objects.get(slug=self.kwargs['productpk'])
    #     return context

    def get_success_url(self):
        return reverse_lazy('')


class FullSaleView(LoginRequiredMixin, UpdateView):
    model = Sale
    form_class = FullSaleForm
    template_name = 'page-sale-full.html'

    def get_success_url(self):
        return reverse_lazy('')