from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from .models import MassificadoGroups
from .forms import MassificadoGroupsEditForm
from product.models import Product


class EntrieProfileNewView(LoginRequiredMixin, CreateView):
    model = MassificadoGroups
    form_class = MassificadoGroupsEditForm
    template_name = 'page-entries-profile.html'

    def get_success_url(self):
        return reverse_lazy('entries-profiles')

    def get_context_data(self, **kwargs):
        context = super(EntrieProfileNewView, self).get_context_data(**kwargs)
        context['products_f'] = Product.objects.filter(kind_person='F')
        context['products_j'] = Product.objects.filter(kind_person='J')
        return context


class EntrieProfileEditView(LoginRequiredMixin, UpdateView):
    model = MassificadoGroups
    form_class = MassificadoGroupsEditForm
    context_object_name = 'profile'
    template_name = 'page-entries-profile.html'

    def get_success_url(self):
        return reverse_lazy('entries-profiles')

    def get_context_data(self, **kwargs):
        context = super(EntrieProfileEditView, self).get_context_data(**kwargs)
        context['products_f'] = Product.objects.filter(kind_person='F')
        context['products_j'] = Product.objects.filter(kind_person='J')
        return context
