# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
# from django.db import transaction
from django.core.paginator import Paginator
# from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from .models import Sale, Partner, Buyer, Status, ResponseDetail, ResponseDeadline
from .forms import BuyerForm, AddressBuyerFormset, FileDeadlineFormset, DeadlineSaleFormset, DetailDeadlineFormset
from product.models import Product, Question


class ProductionView(LoginRequiredMixin, ListView):
    context_object_name = 'sales'
    template_name = 'page-production.html'

    def get_queryset(self):
        # todo: filter sales by the user and his permissions
        sales = Sale.objects.all()
        return Paginator(sales, 1000).page(1)


class CreateBuyerView(LoginRequiredMixin, CreateView):
    model = Buyer
    form_class = BuyerForm
    template_name = 'page-sale.html'
    context_object_name = 'buyer'

    def get_context_data(self, **kwargs):
        data = super(CreateBuyerView, self).get_context_data(**kwargs)
        data['productpk'] = self.kwargs['productpk']
        data['addressbuyer'] = AddressBuyerFormset()
        data['show_all'] = False
        product = Product.objects.get(pk=self.kwargs['productpk'])
        data['status_deadline'] = product.begin_status
        if not product.is_lead:
            data['show_all'] = True
            data['deadlinesale'] = DeadlineSaleFormset()
            data['filedeadline'] = FileDeadlineFormset()
            data['questiondeadline'] = product.profile.question_set.filter(
                type_profile='pdl').order_by('order_number')
            data['detail_deadline'] = DetailDeadlineFormset()
            data['question_detail'] = product.profile.question_set.filter(
                type_profile='pdt').order_by('order_number')

        return data

    def form_valid(self, form):
        response = super(CreateBuyerView, self).form_valid(form)
        addresses = AddressBuyerFormset(self.request.POST)

        for form in addresses.forms:
            if form.is_valid():
                form.instance.buyer = self.object
                form.save()

        sale = Sale()
        sale.product = Product.objects.get(pk=self.request.POST['productpk'])
        sale.buyer = self.object
        # todo: Tirar esse hardcode do pértinêr
        sale.partner = Partner.objects.get(id=1)
        sale.save()

        deadline = DeadlineSaleFormset(self.request.POST)
        for form in deadline.forms:
            if form.is_valid():
                form.instance.sale = sale
                form.save()

                for k, v in self.request.POST.iteritems():
                    if k.split('-')[0] == 'q_resp':
                        q = Question.objects.get(id=k.split('-')[1])
                        response_deadline = ResponseDeadline(
                            question=q,
                            value=v,
                            deadline=form.instance
                        )
                        response_deadline.save()

                details = DetailDeadlineFormset(self.request.POST, instance=form.instance)
                for detail_form in details.forms:
                    if detail_form.is_valid():
                        detail_form.save()

                files = FileDeadlineFormset(self.request.POST, instance=form.instance)
                for file_form in files.forms:
                    if file_form.is_valid():
                        file_form.save()

        return response

    def get_success_url(self):
        # todo: if "permissions" to redirect to determineted url
        return reverse_lazy('index_view')


class EditBuyerView(LoginRequiredMixin, UpdateView):
    model = Buyer
    form_class = BuyerForm
    template_name = 'page-sale.html'
    context_object_name = 'buyer'

    def get_context_data(self, **kwargs):
        data = super(EditBuyerView, self).get_context_data(**kwargs)
        data['addressbuyer'] = AddressBuyerFormset(instance=self.object)
        data['show_all'] = False
        if not Product.objects.get(pk=self.kwargs['productpk']).is_lead:
            data['show_all'] = True
            sale = self.object.sale_set.all()[0]
            data['deadlinesale'] = DeadlineSaleFormset(instance=sale)
            if sale.deadline_set.all():
                data['filedeadline'] = FileDeadlineFormset(instance=sale.deadline_set.all()[0])
            else:
                data['filedeadline'] = FileDeadlineFormset()

            if sale.deadline_set.all():
                data['detail_deadline'] = DetailDeadlineFormset(instance=sale.deadline_set.all()[0])
            else:
                data['detail_deadline'] = DetailDeadlineFormset()

            questions_deadlines = sale.product.profile.question_set.filter(
                type_profile='pdl').order_by('order_number')

            if sale.deadline_set.all():
                deadline = sale.deadline_set.all()[0]
                data['responsequestiondeadline'] = {}
                for quest in questions_deadlines:
                    if quest.responsedeadline_set.filter(deadline=deadline).exists():
                        quest.value = quest.responsedeadline_set.get(
                            deadline=deadline).value

            data['questiondeadline'] = questions_deadlines
        return data

    def form_valid(self, form):
        response = super(EditBuyerView, self).form_valid(form)
        addresses = AddressBuyerFormset(
            self.request.POST, instance=self.object)

        for form in addresses.forms:
            if form.is_valid():
                form.save()
        sale = self.object.sale_set.all()[0]
        deadline = DeadlineSaleFormset(self.request.POST, instance=sale)
        for form in deadline.forms:
            if form.is_valid():
                form.save()

                for k, v in self.request.POST.iteritems():
                    if k.split('-')[0] == 'q_resp':
                        q = Question.objects.get(id=k.split('-')[1])
                        ResponseDeadline.objects.update_or_create(
                            question=q,
                            deadline=form.instance,
                            defaults={'value': v}
                        )

                details = DetailDeadlineFormset(self.request.POST, instance=form.instance)
                for detail_form in details.forms:
                    if detail_form.is_valid():
                        detail_form.save()

                files = FileDeadlineFormset(self.request.POST, self.request.FILES, instance=form.instance)
                for file_form in files.forms:
                    if file_form.is_valid():
                        file_form.save()

        return response

    def get_success_url(self):
        # todo: if "permissions" to redirect to determineted url
        return reverse_lazy('index_view')
