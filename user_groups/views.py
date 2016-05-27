from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from .models import MassificadoGroups
from .forms import MassificadoGroupsEditForm
from product.models import Product, Status, FileType


class EntrieProfileNewView(CreateView):
    pass


class EntrieProfileEditView(LoginRequiredMixin, UpdateView):
    model = MassificadoGroups
    form_class = MassificadoGroupsEditForm
    context_object_name = 'profile'
    template_name = 'page-entries-profile.html'

    def get_success_url(self):
        return reverse_lazy('entries-profiles')

    def get_context_data(self, **kwargs):
        context = super(EntrieProfileEditView, self).get_context_data(**kwargs)
        context['products_f'] = list(Product.objects.filter(kind_person='J'))
        context['products_j'] = list(Product.objects.filter(kind_person='F'))
        context['products'] = list(Product.objects.all())
        context['status'] = Status.objects.all()
        context['files'] = FileType.objects.all()
        # context['profiles'] = Profiles.objects.all()
        return context
