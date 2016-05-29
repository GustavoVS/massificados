# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from .models import Sale, Partner, Buyer, BuyerAddress, Status, ResponseDeadline
from .forms import BuyerForm, AddressBuyerFormset, FileDeadlineFormset, DeadlineSaleFormset, DetailDeadlineFormset
from product.models import Product, Question
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BuyerSerializer, BuyerAddressSerializer



class ProductionView(LoginRequiredMixin, ListView):
    context_object_name = 'sales'
    template_name = 'page-production.html'

    def get_queryset(self):
        # todo: filter sales by the user and his permissions
        if not self.request.user.group_permissions:
            sales = Sale.objects.all()
        else:
            sales = Sale.objects.filter(
                product__in=self.request.user.group_permissions.product.all(),
                deadline__status__in=self.request.user.group_permissions.status_see.all(),
                owner__group_permissions__in=self.request.user.group_permissions.profiles.all()
            )
        return Paginator(sales, 1000).page(1)


class CreateBuyerView(LoginRequiredMixin, CreateView):
    model = Buyer
    form_class = BuyerForm
    template_name = 'page-sale.html'
    context_object_name = 'buyer'

    def get_context_data(self, **kwargs):
        data = super(CreateBuyerView, self).get_context_data(**kwargs)
        product = Product.objects.get(pk=self.kwargs['productpk'])
        data['product'] = product
        data['addressbuyer'] = AddressBuyerFormset()
        data['show_all'] = False
        data['status_deadline'] = product.begin_status
        # data['possible_new_status'] = Status.objects.filter(level__gte=product.begin_status.level).select_related()
        data['possible_new_status'] = self.request.user.group_permissions.status_set.filter(
            level__gte=product.begin_status.level).select_related()
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
                form.instance   .buyer = self.object
                form.save()

        sale = Sale()
        sale.product = Product.objects.get(pk=self.request.POST['productpk'])
        sale.buyer = self.object
        sale.owner = self.request.user
        sale.partner = Partner.objects.get(id=1)
        sale.save()

        deadline = DeadlineSaleFormset(self.request.POST)
        for form in deadline.forms:
            if form.is_valid():
                form.instance.sale = sale
                form.save()

                # if self.request.POST.get('new-status', ''):
                #     dl.status_id = self.request.POST.get('new-status', '')
                #     dl.save()

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
        data['product'] = Product.objects.get(pk=self.kwargs['productpk'])
        data['sale'] = sale = self.object.sale_set.all()[0]
        if not Product.objects.get(pk=self.kwargs['productpk']).is_lead:
            data['show_all'] = True
            data['deadlinesale'] = DeadlineSaleFormset(instance=sale)
            data['status_deadline'] = sale.deadline_set.all()[0].status
            # todo: filter user permissions
            data['possible_new_status'] = Status.objects.filter(
                level__gte=sale.deadline_set.all()[0].status.level).order_by('level')
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
                # form.object.status_id = self.request.POST.get('new-status', '')
                dl = form.save()
                if self.request.POST.get('new-status', ''):
                    dl.status_id = self.request.POST.get('new-status', '')
                    dl.save()

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


@api_view(['GET', ])
def user_cnpj(request):
    if request.method == 'GET':
        try:
            buyer = Buyer.objects.get(cpf_cnpj=request.GET.get('cpf_cnpj'))
            buyer_serialize = BuyerSerializer(buyer)

            buyeraddress = BuyerAddress.objects.get(buyer=buyer)
            buyeraddress_serialize = BuyerAddressSerializer(buyeraddress)

            resp = dict(buyer_serialize.data)
            for k, v in dict(buyeraddress_serialize.data).iteritems():
                resp[k] = v
            return Response(resp)
        except Buyer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
