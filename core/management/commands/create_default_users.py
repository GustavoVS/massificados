# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria usuários default para o início da aplicação'

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", "boasenha2016#")

        if not User.objects.filter(username="demo").exists():
            u = User(username="demo", email="demo@demo.com", password="massificadodemo")
            u.save()