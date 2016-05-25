# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class UserAdmin(UserAdmin):
    model = User

admin.site.register(User, UserAdmin)
admin.site.register(MassificadoGroups)
admin.site.register(Profiles)
