# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from .models import Sale, Partner, Buyer, Status
from .forms import BuyerForm, AddressBuyerFormset
from product.models import Product


class ProductionView(LoginRequiredMixin, ListView):
    context_object_name = 'sales'
    template_name = 'page-production.html'

    def get_queryset(self):
        # todo: filter sales by the user and his permissions
        # sale_page = Paginator(Sale.objects.all(), 1000)
        return Paginator(Sale.objects.all(), 1000).page(1)


class CreateBuyerView(LoginRequiredMixin, CreateView):
    model = Buyer
    form_class = BuyerForm
    template_name = 'page-sale.html'

    def get_context_data(self, **kwargs):
        data = super(CreateBuyerView, self).get_context_data(**kwargs)
        data['productpk'] = self.kwargs['productpk']
        data['addressbuyer'] = AddressBuyerFormset()
        return data

    def form_valid(self, form):
        response = super(CreateBuyerView, self).form_valid(form)
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


class EditBuyerView(LoginRequiredMixin, UpdateView):
    model = Buyer
    form_class = BuyerForm
    template_name = 'page-sale.html'

    def get_context_data(self, **kwargs):
        data = super(EditBuyerView, self).get_context_data(**kwargs)
        data['addressbuyer'] = AddressBuyerFormset()
        return data

    def form_valid(self, form):
        response = super(EditBuyerView, self).form_valid(form)
        addresses = AddressBuyerFormset(self.request.POST)
        if addresses.is_valid():
            addresses.instance.buyer = self.object
            addresses.save()
        return response

    def get_success_url(self):
        return reverse_lazy('index_view')


class EditProductProfileView(LoginRequiredMixin, DetailView):
    model = Sale
    # form_class = ProductProfileForm
    template_name = 'page-sale-product-view.html'