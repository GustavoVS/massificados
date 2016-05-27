from django.contrib import admin

from .models import ActionStatusEmails, ActionStatusEmailsUsers

admin.site.register(ActionStatusEmails)
admin.site.register(ActionStatusEmailsUsers)
