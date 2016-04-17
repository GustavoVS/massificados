from django.template.response import TemplateResponse
# Create your views here.

def IndexView(request):
    return TemplateResponse(request, 'index.html')