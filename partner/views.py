# -*- coding: utf-8 -*-
from django.views.generic import ListView
from partner.models import Sac, Partner


class SacsListView(ListView):
    context_object_name = 'sacs'
    template_name = 'page-sacs.html'
    def get_queryset(self):
        # sac = Sac.objects.all()
        return Sac.objects.all
        # todo: permissions


