# -*- coding: utf-8 -*-
from django.views.generic import ListView
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.encoding import smart_str
# from massificados.settings import MEDIA_ROOT


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
        # context['products_f'] = list(Product.objects.filter(kind_person='F'))*3
        # context['products_j'] = list(Product.objects.filter(kind_person='J'))*2
        # context['products'] = Product.objects.all()
        if self.request.user.is_authenticated():
            context['products_f'] = self.request.user.group_permissions.product.filter(kind_person='F')
            context['products_j'] = self.request.user.group_permissions.product.filter(kind_person='J')
        return context


class EntriesView(LoginRequiredMixin, MassificadoPageListView):
    context_object_name = 'cadastros'
    template_name = 'page-entries.html'

    def get_queryset(self):
        return self.request.user.user_permissions.all()

# def download_media(request, *args, **kwargs):
#     # import ipdb; ipdb.set_trace()
#     file_name = kwargs['file_name']
#     file_path = MEDIA_ROOT + '/' + file_name
#     file_wrapper = FileWrapper(file(file_path,'rb'))
#     file_mimetype = mimetypes.guess_type(file_path)
#     response = HttpResponse(file_wrapper, content_type=file_mimetype )
#     response['X-Sendfile'] = file_path
#     response['Content-Length'] = os.stat(file_path).st_size
#     response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
#     return response
# def download_media(request, **kwargs):
#     file_name = kwargs['file_name']
#     import ipdb; ipdb.set_trace()
#     path_to_file = "/media/{0}".format(file_name)
#     response = HttpResponse(content_type='image/jpg')
#     response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
#     response['X-Sendfile'] = smart_str(path_to_file)
#     return response
# def download_media(request, **kwargs):
#     valid_image = MEDIA_ROOT + kwargs['file_name']
#     import ipdb; ipdb.set_trace()
#     try:
#         with open(valid_image, "rb") as f:
#             return HttpResponse(f.read(), content_type="image/jpeg")
#     except IOError:
#         red = Image.new('RGBA', (1, 1), (255,0,0,0))
#         response = HttpResponse(content_type="image/jpeg")
#         red.save(response, "JPEG")
#         return response
