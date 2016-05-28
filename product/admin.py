# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

admin.site.register(InsuranceCompany)
admin.site.register(Bank)
admin.site.register(Branch)
admin.site.register(FileType)
admin.site.register(FileTypeSee)
admin.site.register(FileTypeDownload)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Domain)
admin.site.register(MethodPayment)
admin.site.register(Status)
# admin.site.register(StatusSet)
# admin.site.register(StatusEdit)
# admin.site.register(StatusSee)
# admin.site.register(StatusPermission)
admin.site.register(ActionStatus)