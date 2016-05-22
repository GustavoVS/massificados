# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from partner.models import Partner
from product.models import Status, FileType, InsuranceCompany, Branch

User = get_user_model()

DEFAULT_STATUS = (
    'Apólice Gerada', 'Repasse pago', 'Pago Pela Seguradora', 'Cotação de Garantia Negada',
    'Cotação de Garantia Aprovada', 'Cotação de Garantia Gerada', 'Solicitação de Cotação de Garantia',
    'Lead de Garantia Gerado', 'Cotação de Benefícios Negada', 'Cotação de Benefícios Aprovada',
    'Cotação de Benefícios Gerada', 'Solicitação de Cotação de Benefícios', 'Aberto',
    'Lead de benefícios Gerado', 'Boleto Gerado', 'Proposta Gerada'
)

DEFAULT_FILES = ('Proposta de Endosso', 'Proposta de Apólice', 'Endosso', 'Apólice', 'Boleto de Apólice',
                 'Boleto de Endosso')

DEFAULT_CIA = (('Tokyo', '123456'),)

DEFAULT_BRANCH = ('Vida',)


class Command(BaseCommand):
    help = 'Cria usuários default para o início da aplicação'

    def handle(self, *args, **options):

        if Partner.objects.filter(id=1).exists():
            p = Partner.objects.get(id=1)
        else:
            s = Site(domain='sofisa', name='Sofisa')
            s.save()
            p = Partner(
                name='Sofisa',
                email='sofisa@mail.com',
                cnpj='60.889.128.0001-80',
                site=s,
            )
            p.save()

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", "boasenha2016#", partner=p)

        if not User.objects.filter(username="demo").exists():
            u = User(username="demo", email="demo@demo.com", password="massificadodemo", partner=p)
            u.save()

        if not Status.objects.filter(id=1).exists():
            for status_name in DEFAULT_STATUS:
                st = Status(name=status_name)
                st.save()

        if not FileType.objects.filter(id=1).exists():
            for file_name in DEFAULT_FILES:
                fl = FileType(name=file_name)
                fl.save()

        if not InsuranceCompany.objects.filter(id=1).exists():
            for cia, susep in DEFAULT_CIA:
                insurance_company = InsuranceCompany(name=cia, susep=susep)
                insurance_company.save()

        if not Branch.objects.filter(id=1).exists():
            for branch_name in DEFAULT_BRANCH:
                branch = Branch(name=branch_name)
                branch.save()
