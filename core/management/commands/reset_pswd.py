# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria usuários default para o início da aplicação'

    def handle(self, *args, **options):

        for user in User.objects.all():
            user.set_password('x')
            user.email = user.email + '.development'
            user.save()
