# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from partner.models import Partner
from product.models import Status, StatusSee, StatusEdit, StatusSet, StatusInitial, FileType, FileTypeSee, FileTypeDownload, InsuranceCompany, Branch, Product, Profile
from user_account.models import Permissions, MassificadoGroups

User = get_user_model()

DEFAULT_STATUS = (
    'Aberto',
    'Apólice Gerada', 'Proposta Gerada', 'Proposta Cancelada',
    'Cotação de Garantia Negada', 'Cotação de Garantia Aprovada', 'Cotação de Garantia Gerada', 'Solicitação de Cotação de Garantia',
    'Lead de Garantia Gerado',
    'Cotação de Benefícios Negada', 'Cotação de Benefícios Aprovada', 'Cotação de Benefícios Gerada', 'Solicitação de Cotação de Benefícios',
    'Lead de Benefícios Gerado',
    'Repasse Pago', 'Repasse Pendente', 'Pago Pela Seguradora',
    'Boleto Gerado',
)

DEFAULT_STATUS_PRODUCT_TOKIO = ('Aberto', 'Proposta Gerada', 'Proposta Cancelada', 'Boleto Gerado', 'Apólice Gerada', 'Repasse Pendente', 'Repasse Pago', 'Pago Pela Seguradora')

DEFAULT_STATUS_PRODUCT_GARANTIA = (
    'Aberto', 'Boleto Gerado',
    'Lead de Garantia Gerado', 'Cotação de Garantia Negada', 'Cotação de Garantia Aprovada', 'Cotação de Garantia Gerada', 'Solicitação de Cotação de Garantia',
    'Apólice Gerada', 'Repasse Pendente', 'Repasse Pago', 'Pago Pela Seguradora'
)

DEFAULT_FILES = ('Proposta de Endosso', 'Proposta de Apólice', 'Endosso', 'Apólice', 'Boleto de Apólice',
                 'Boleto de Endosso',)

DEFAULT_CIA = (('Tokio', '123456'), ('GalCorr', '000000'), )

DEFAULT_BRANCH = ('Vida', 'Acidentes Pessoais', 'Garantia Tradicional', 'Garantia Judicial', 'Fiança Locatícia', )

DEFAULT_PROFILE = ('Perfil Vida', 'Perfil Vida Global', 'Perfil Acidentes Pessoais', 'Perfil Garantia Tradicional', 'Perfil Garantia Judicial', 'Perfil Fiança Locatícia', )

DEFAULT_PRODUCT_NAME_GALCORR = ('Vida', 'Vida Global', 'Acidentes Pessoais', 'Garantia Tradicional', 'Garantia Judicial', 'Fiança Locatícia')

DEFAULT_PRODUCT_NAME_PARTNER = ('Vida', 'Vida Global', 'Acidentes Pessoais', 'Garantia Tradicional', 'Garantia Judicial', 'Fiança Locatícia')

DEFAULT_PRODUCT_NAME_INSURANCE = ('Vida', 'Vida Global', 'Acidentes Pessoais', )

DEFAULT_PRODUCT = (('Vida', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Vida', DEFAULT_FILES, 'Aberto', 'Perfil Vida', DEFAULT_STATUS_PRODUCT_TOKIO, ),
                   ('Vida Global', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Vida', DEFAULT_FILES, 'Aberto', 'Perfil Vida Global', DEFAULT_STATUS_PRODUCT_TOKIO, ),
                   ('Acidentes Pessoais', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Acidentes Pessoais', DEFAULT_FILES, 'Aberto', 'Perfil Acidentes Pessoais', DEFAULT_STATUS_PRODUCT_TOKIO, ),
                   ('Garantia Tradicional', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Garantia Tradicional', DEFAULT_FILES, 'Aberto', 'Perfil Garantia Tradicional', DEFAULT_STATUS_PRODUCT_GARANTIA, ),
                   ('Garantia Judicial', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Garantia Judicial', DEFAULT_FILES, 'Aberto', 'Perfil Garantia Judicial', DEFAULT_STATUS_PRODUCT_GARANTIA, ),
                   ('Fiança Locatícia', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Fiança Locatícia', DEFAULT_FILES, 'Aberto', 'Perfil Fiança Locatícia', DEFAULT_STATUS_PRODUCT_GARANTIA, ),
                   )

DEFAULT_PROFILE_NAME = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Administrador',
    'Perfil GalCorr Gerencial',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
    'Perfil GalCorr Técnico Garantia',
    'Perfil GalCorr Financeiro',
    'Perfil Tokio'
)

DEFAULT_PROFILE_PERMISSION = (('Perfil Parceiro Diretor', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil Parceiro Supervisor', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil Parceiro Gerente', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil Parceiro Administrador', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Administrador', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Gerencial', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Comercial', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Operacional', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Técnico Benefícios', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Técnico Garantia', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Financeiro', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil Tokio', '1', '1', '1', '1', '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS_PRODUCT_TOKIO, DEFAULT_STATUS_PRODUCT_TOKIO, DEFAULT_STATUS_PRODUCT_TOKIO, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ), )


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

        for status_name in DEFAULT_STATUS:
            if not Status.objects.filter(name=status_name).exists():
                st = Status(name=status_name)
                st.save()

        for status_name in DEFAULT_STATUS:
            if not StatusSee.objects.filter(name=status_name).exists():
                st = StatusSee(name=status_name)
                st.save()

        for status_name in DEFAULT_STATUS:
            if not StatusEdit.objects.filter(name=status_name).exists():
                st = StatusEdit(name=status_name)
                st.save()

        for status_name in DEFAULT_STATUS:
            if not StatusSet.objects.filter(name=status_name).exists():
                st = StatusSet(name=status_name)
                st.save()

        for status_name in DEFAULT_STATUS:
            if not StatusInitial.objects.filter(name=status_name).exists():
                st = StatusInitial(name=status_name)
                st.save()

        for file_name in DEFAULT_FILES:
            if not FileType.objects.filter(name=file_name).exists():
                fl = FileType(name=file_name)
                fl.save()

        for file_name in DEFAULT_FILES:
            if not FileTypeSee.objects.filter(name=file_name).exists():
                fl = FileTypeSee(name=file_name)
                fl.save()

        for file_name in DEFAULT_FILES:
            if not FileTypeDownload.objects.filter(name=file_name).exists():
                fl = FileTypeDownload(name=file_name)
                fl.save()

        for cia, susep in DEFAULT_CIA:
            if not InsuranceCompany.objects.filter(name=cia).exists():
                insurance_company = InsuranceCompany(name=cia, susep=susep)
                insurance_company.save()

        for branch_name in DEFAULT_BRANCH:
            if not Branch.objects.filter(name=branch_name).exists():
                branch = Branch(name=branch_name)
                branch.save()

        for profile_name in DEFAULT_PROFILE:
            if not Profile.objects.filter(name=profile_name).exists():
                pe = Profile(name=profile_name)
                pe.save()

        for product_name, introduction, description, declaration, kind, insurance, branch, files,\
        begin, profile, status_active in DEFAULT_PRODUCT:
            if not Product.objects.filter(name=product_name).exists():
                product = Product(
                    name=product_name,
                    introduction=introduction,
                    description=description,
                    declaration=declaration,
                    kind_person=kind,
                    insurance_company=InsuranceCompany.objects.get(name=insurance),
                    branch=Branch.objects.get(name=branch),
                    begin_status=StatusInitial.objects.get(name=begin),
                    profile=Profile.objects.get(name=profile)
                )

                product.save()
                for file in files:
                    product.file_type.add(FileType.objects.get(name=file))

                for status in status_active:
                    product.status_permission.add(Status.objects.get(name=status))

        for permission in DEFAULT_PROFILE_NAME:
            if not Permissions.objects.filter(name=permission).exists():
                per = Permissions(name=permission)
                per.save()

        for permission_name, menu_active_product, menu_active_dashboard, menu_active_production, menu_active_entries, menu_active_notification, menu_active_profile,\
                products_permission, status_see_permission, status_edit_permission, status_set_permission, filetype_see_permission, filetype_download_permission, profile_names_permission \
                in DEFAULT_PROFILE_PERMISSION:
            group = MassificadoGroups(
                name=permission_name,
                menu_products=menu_active_product,
                menu_dashboard=menu_active_dashboard,
                menu_production=menu_active_production,
                menu_entries=menu_active_entries,
                menu_notification=menu_active_notification,
                menu_profile=menu_active_profile
            )

            group.save()
            for products_p in products_permission:
                group.product.add(Product.objects.get(name=products_p))

            for status_see_p in status_see_permission:
                group.status_see.add(StatusSee.objects.get(name=status_see_p))

            for status_edit_p in status_edit_permission:
                group.status_edit.add(StatusEdit.objects.get(name=status_edit_p))

            for status_set_p in status_set_permission:
                group.status_set.add(StatusSet.objects.get(name=status_set_p))

            for filetype_see_p in filetype_see_permission:
                group.filetype_see.add(FileTypeSee.objects.get(name=filetype_see_p))

            for filetype_download_p in filetype_download_permission:
                group.filetype_download.add(FileTypeDownload.objects.get(name=filetype_download_p))

            for profile_names_p in profile_names_permission:
                group.permissions.add(Permissions.objects.get(name=profile_names_p))
