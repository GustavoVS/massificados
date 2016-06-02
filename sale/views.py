# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from .models import Sale, Partner, Buyer, BuyerAddress, Status, ResponseDeadline, Quote, SubQuote, File
from .forms import BuyerForm, AddressBuyerFormset, DeadlineSaleFormset
from product.models import Product, Question
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BuyerSerializer, BuyerAddressSerializer
from django.utils.datastructures import MultiValueDictKeyError


class ProductionView(LoginRequiredMixin, ListView):
    context_object_name = 'sales'
    template_name = 'page-production.html'

    def get_queryset(self):
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
        data['rules'] = product.rules.all()
        data['addressbuyer'] = AddressBuyerFormset()
        data['status_deadline'] = product.begin_status
        data['possible_new_status'] = self.request.user.group_permissions.status_set.filter(
            level__gte=product.begin_status.level).select_related()
        data['show_all'] = True
        data['deadlinesale'] = DeadlineSaleFormset()
        data['sample_file_type'] = product.sample_file_type.all()
        # data['filedeadline'] = FileDeadlineFormset(product.file_type.all())
        data['questiondeadline'] = product.profile.question_set.filter(
            type_profile='pdl').order_by('order_number')
        # data['detail_deadline'] = DetailDeadlineFormset()
        data['question_detail'] = product.profile.question_set.filter(
            type_profile='pdt').order_by('order_number')

        num_files = product.sample_file_type.all().count()
        if num_files % 4 == 0:
            data['sample_file_type_cols'] = 3
        elif num_files % 3 == 0:
            data['sample_file_type_cols'] = 4
        elif num_files % 2 == 0:
            data['sample_file_type_cols'] = 6
        elif num_files == 1:
            data['sample_file_type_cols'] = 12

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
                dl = form.instance
                # se isso for virar um modelo de negócio para nós, refatorar as comissões abaixo, WS
                # comissão do partner
                if Quote.objects.filter(deadline=dl).exists():
                    quote = Quote.objects.get(deadline=dl)
                else:
                    quote = Quote(deadline=dl,)
                    quote.value = dl.payment * (dl.sale.product.partner_percentage / 100)
                    quote.percentage = dl.sale.product.partner_percentage
                    quote.save()

                # repasse do owner
                if SubQuote.objects.filter(quote=quote, user=dl.sale.owner).exists():
                    subquote = SubQuote.objects.get(quote=quote, user=dl.sale.owner)
                else:
                    subquote = SubQuote(quote=quote, user=dl.sale.owner,)
                    subquote.value = dl.payment * (dl.sale.product.owner_percentage / 100)
                    subquote.percentage = dl.sale.product.owner_percentage
                    subquote.save()

                # repasse do owner.master
                if dl.sale.owner.master:
                    if SubQuote.objects.filter(quote=quote, user=dl.sale.owner.master).exists():
                        subquote = SubQuote.objects.get(quote=quote, user=dl.sale.owner.master)
                    else:
                        subquote = SubQuote(quote=quote, user=dl.sale.owner.master)
                        subquote.value = dl.payment * (dl.sale.product.master_percentage / 100)
                        subquote.percentage = dl.sale.product.master_percentage
                        subquote.save()

                # repasse do owner.director
                if dl.sale.owner.director:
                    if SubQuote.objects.filter(quote=quote, user=dl.sale.owner.director).exists():
                        subquote = SubQuote.objects.get(quote=quote, user=dl.sale.owner.director)
                    else:
                        subquote = SubQuote(quote=quote, user=dl.sale.owner.director)
                        subquote.value = dl.payment * (dl.sale.product.director_percentage / 100)
                        subquote.percentage = dl.sale.product.director_percentage
                        subquote.save()

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

                # details = DetailDeadlineFormset(self.request.POST, instance=form.instance)
                # for detail_form in details.forms:
                #     if detail_form.is_valid():
                #         detail_form.save()

                # files = FileDeadlineFormset(self.request.POST, instance=form.instance)
                # for file_form in files.forms:
                #     if file_form.is_valid():
                #         file_form.save()

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
        # if not Product.objects.get(pk=self.kwargs['productpk']).is_lead:
        data['deadline'] = sale.deadline_set.all()[0]
        data['show_all'] = True
        data['deadlinesale'] = DeadlineSaleFormset(instance=sale)
        data['sample_file_type'] = sale.product.sample_file_type.all()
        data['rules'] = sale.product.rules.all()
        num_files = sale.product.sample_file_type.all().count()
        if num_files % 4 == 0:
            data['sample_file_type_cols'] = 3
        elif num_files % 3 == 0:
            data['sample_file_type_cols'] = 4
        elif num_files % 2 == 0:
            data['sample_file_type_cols'] = 6
        elif num_files == 1:
            data['sample_file_type_cols'] = 12
        data['uploaded_files'] = sale.deadline_set.all()[0].file_set.all()
        data['uploaded_file_types'] = [file_up.file_type for file_up in sale.deadline_set.all()[0].file_set.all()]
        data['possible_new_status'] = self.request.user.group_permissions.status_set.filter(
            level__gte=sale.deadline_set.all()[0].status.level).order_by('level')
        # data['possible_new_status'] = Status.objects.filter(
        #     level__gte=sale.deadline_set.all()[0].status.level).order_by('level')
        # if sale.deadline_set.all():
        #     data['filedeadline'] = FileDeadlineFormset(sale.product.file_type.all(), instance=sale.deadline_set.all()[0])
        # else:
        #     data['filedeadline'] = FileDeadlineFormset(sale.product.file_type.all())

        # if sale.deadline_set.all():
        #     data['detail_deadline'] = DetailDeadlineFormset(instance=sale.deadline_set.all()[0])
        # else:
        #     data['detail_deadline'] = DetailDeadlineFormset()

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

                # se isso for virar um modelo de negócio para nós, refatorar as comissões abaixo, WS
                # comissão do partner
                if Quote.objects.filter(deadline=dl).exists():
                    quote = Quote.objects.get(deadline=dl)
                else:
                    quote = Quote(deadline=dl,)
                    quote.value = dl.payment * (dl.sale.product.partner_percentage / 100)
                    quote.percentage = dl.sale.product.partner_percentage
                    quote.save()

                # repasse do owner
                if SubQuote.objects.filter(quote=quote, user=dl.sale.owner).exists():
                    subquote = SubQuote.objects.get(quote=quote, user=dl.sale.owner)
                else:
                    subquote = SubQuote(quote=quote, user=dl.sale.owner,)
                    subquote.value = dl.payment * (dl.sale.product.owner_percentage / 100)
                    subquote.percentage = dl.sale.product.owner_percentage
                    subquote.save()

                # repasse do owner.master
                if dl.sale.owner.master:
                    if SubQuote.objects.filter(quote=quote, user=dl.sale.owner.master).exists():
                        subquote = SubQuote.objects.get(quote=quote, user=dl.sale.owner.master)
                    else:
                        subquote = SubQuote(quote=quote, user=dl.sale.owner.master)
                        subquote.value = dl.payment * (dl.sale.product.master_percentage / 100)
                        subquote.percentage = dl.sale.product.master_percentage
                        subquote.save()

                # repasse do owner.director
                if dl.sale.owner.director:
                    if SubQuote.objects.filter(quote=quote, user=dl.sale.owner.director).exists():
                        subquote = SubQuote.objects.get(quote=quote, user=dl.sale.owner.director)
                    else:
                        subquote = SubQuote(quote=quote, user=dl.sale.owner.director)
                        subquote.value = dl.payment * (dl.sale.product.director_percentage / 100)
                        subquote.percentage = dl.sale.product.director_percentage
                        subquote.save()

                for k, v in self.request.POST.iteritems():
                    if k.split('-')[0] == 'q_resp':
                        q = Question.objects.get(id=k.split('-')[1])
                        ResponseDeadline.objects.update_or_create(
                            question=q,
                            deadline=form.instance,
                            defaults={'value': v}
                        )

                # details = DetailDeadlineFormset(self.request.POST, instance=form.instance)
                # for detail_form in details.forms:
                #     if detail_form.is_valid():
                #         detail_form.save()

                # files = FileDeadlineFormset(self.request.POST, self.request.FILES, instance=form.instance)
                # for file_form in files.forms:
                #     if file_form.is_valid():
                #         file_form.save()

        return response

    def get_success_url(self):
        # todo: if "permissions" to redirect to determineted url
        return reverse_lazy('index_view')


@api_view(['GET', ])
def user_cnpj(request):
    if request.method == 'GET':
        try:
            buyer = Buyer.objects.filter(cpf_cnpj=request.GET.get('cpf_cnpj')).latest('date_create')
            buyer_serialize = BuyerSerializer(buyer)

            buyeraddress = BuyerAddress.objects.get(buyer=buyer)
            buyeraddress_serialize = BuyerAddressSerializer(buyeraddress)

            resp = dict(buyer_serialize.data)
            for k, v in dict(buyeraddress_serialize.data).iteritems():
                resp[k] = v
            return Response(resp)
        except Buyer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', ])
def upload_media(request):
    msg = url = txt = ''
    deadline_id = request.POST.get('deadline-pk', '')
    file_type_id = request.POST.get('file-type-pk', '')
    try:
        doc = request.FILES['input-file-type']
    except MultiValueDictKeyError:
        doc = False

    if not deadline_id:
        msg = _('An error has occurred')
    elif not file_type_id:
        msg = _('Select a File Type to upload')
    elif not doc:
        msg = _('Select a File')

    if not msg:
        doc.read()
        sale_file = File(
            deadline_id=deadline_id,
            file_type_id=file_type_id,
            document=doc,
            uploaded_by=request.user
        )
        sale_file.save()
        msg = _('Successfully file uploaded')
        url = sale_file.document.url
        txt = _("Uploaded by <b>%s</b> in <small>%s</small>" % (sale_file.uploaded_by, sale_file.upload_date))
        error = False
    else:
        error = True
    return Response(
        {'error': error, 'msg': msg, 'url': url, 'txt': txt},
        content_type="application/json"
    )
