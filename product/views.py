from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from product.models import Product


class ProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'page-products.html'
    context_object_name = 'products'



    def get_queryset(self):

        return Product.objects.all()
