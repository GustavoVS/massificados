# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from partner.models import Partner
from product.models import Status, StatusSee, StatusEdit, StatusSet, StatusPermission, FileType, FileTypeSee, FileTypeDownload, InsuranceCompany, Branch, Product, Profile
from user_account.models import Profiles, MassificadoGroups

User = get_user_model()

DEFAULT_STATUS = (
    # ('Aberto', 1),

    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),

    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),

    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3), ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PRODUCT_TOKIO = (
                                # ('Aberto', 1),
                                ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3), ('Apólice Cancelada', 4), ('Repasse Pago', 4),)
DEFAULT_STATUS_PRODUCT_TOKIO_EMAIL = (
                                      # ('Aberto', 1, ('r.cabral.n@gmail.com', ), ),
                                      ('Proposta Gerada', 1, ('{Gerente}', '{Seguradora}', 'flavio.saraiva@galcorr.com.br' , 'fabiano.costa@galcorr.com.br', ), ),
                                      ('Proposta Cancelada', 2, ('{Gerente}', '{Seguradora}', 'flavio.saraiva@galcorr.com.br' , 'fabiano.costa@galcorr.com.br', ), ),
                                      ('Boleto Gerado', 2, ('{Gerente}', '{Seguradora}', 'flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', ), ),
                                      ('Apólice Gerada', 3, ('{Gerente}', '{Seguradora}', 'flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'lucia.moraes@galcorr.com.br', ), ),
                                      ('Apólice Cancelada', 4, ('{Gerente}', '{Seguradora}', 'flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'lucia.moraes@galcorr.com.br', ), ),
                                      ('Repasse Pago', 4, ('{Gerente}', 'flavio.saraiva@galcorr.com.br', ), ), )

DEFAULT_STATUS_PRODUCT_GARANTIA = (
    # ('Aberto', 1),
    ('Lead de Garantia Gerado', 2), ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
)

DEFAULT_STATUS_PRODUCT_GARANTIA_EMAIL = (
    # ('Aberto', 1, ('r.cabral.n@gmail.com', ), ),
    ('Lead de Garantia Gerado', 2, ('{Gerente}', 'flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', ), ),
    ('Lead de Garantia Cancelado', 2, ('{Gerente}', 'flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', ), ),
    ('Solicitação de Cotação de Garantia', 3, ('flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'rafael.nunes@comercialseguros.com.br', ), ),
    ('Cotação de Garantia Gerada', 4, ('flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'rafael.nunes@comercialseguros.com.br', ), ),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4, ('flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'rafael.nunes@comercialseguros.com.br', ), ),
    ('Cotação de Garantia Negada', 5, ('flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'rafael.nunes@comercialseguros.com.br', '{Gerente}', ), ),
    ('Cotação de Garantia Aprovada', 6, ('flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'rafael.nunes@comercialseguros.com.br', '{Gerente}', ), ),
)

DEFAULT_STATUS_PRODUCT_BENEFICIOS = (
    # ('Aberto', 1),
    ('Lead de Benefícios Gerado', 2),
    ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5),
    ('Cotação de Benefícios Aprovada', 6),
)

DEFAULT_STATUS_PRODUCT_BENEFICIOS_EMAIL = (
    # ('Aberto', 1, ('r.cabral.n@gmail.com', ), ),
    ('Lead de Benefícios Gerado', 2, ('{Gerente}', 'flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', ), ) ,
    ('Lead de Benefícios Cancelado', 2, ('{Gerente}', 'flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', ) , ),
    ('Solicitação de Cotação de Benefícios', 3, ('flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'adriano.telles@galcorr.com.br', ), ),
    ('Cotação de Benefícios Gerada', 4, ('flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'adriano.telles@galcorr.com.br', ), ),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4, ('flavio.saraiva@galcorr.com.br', 'adriano.telles@galcorr.com.br', 'rafael.nunes@galcorr.com.br', ), ),
    ('Cotação de Benefícios Negada', 5, ('flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'adriano.telles@galcorr.com.br', '{Gerente}', ), ),
    ('Cotação de Benefícios Aprovada', 6, ('flavio.saraiva@galcorr.com.br', 'fabiano.costa@galcorr.com.br', 'adriano.telles@galcorr.com.br', '{Gerente}', ), ),
)

DEFAULT_FILES = ('Proposta de Endosso', 'Proposta de Apólice', 'Endosso', 'Apólice', 'Boleto de Apólice',
                 'Boleto de Endosso',)

DEFAULT_CIA = (('Tokio', '123456'), ('GalCorr', '000000'), )

DEFAULT_BRANCH = ('Vida', 'Acidentes Pessoais', 'Garantia Tradicional', 'Garantia Judicial', 'Fiança Locatícia', )

DEFAULT_PROFILE = ('Perfil Vida', 'Perfil Vida Global', 'Perfil Acidentes Pessoais', 'Perfil Garantia Tradicional', 'Perfil Garantia Judicial', 'Perfil Fiança Locatícia', )

DEFAULT_PRODUCT_NAME_GALCORR = ('Vida', 'Vida Global', 'Acidentes Pessoais', 'Garantia Tradicional', 'Garantia Judicial', 'Fiança Locatícia')

DEFAULT_PRODUCT_NAME_PARTNER = ('Vida', 'Vida Global', 'Acidentes Pessoais', 'Garantia Tradicional', 'Garantia Judicial', 'Fiança Locatícia')

DEFAULT_PRODUCT_NAME_INSURANCE = ('Vida', 'Vida Global', 'Acidentes Pessoais', )

DEFAULT_PRODUCT = (('Vida', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Vida', DEFAULT_FILES, 'Proposta Gerada', 'Perfil Vida', DEFAULT_STATUS_PRODUCT_TOKIO, ),
                   ('Vida Global', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Vida', DEFAULT_FILES, 'Proposta Gerada', 'Perfil Vida Global', DEFAULT_STATUS_PRODUCT_TOKIO, ),
                   ('Acidentes Pessoais', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Acidentes Pessoais', DEFAULT_FILES, 'Proposta Gerada', 'Perfil Acidentes Pessoais', DEFAULT_STATUS_PRODUCT_TOKIO, ),
                   ('Garantia Tradicional', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Garantia Tradicional', DEFAULT_FILES, 'Lead de Garantia Gerado', 'Perfil Garantia Tradicional', DEFAULT_STATUS_PRODUCT_GARANTIA, ),
                   ('Garantia Judicial', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Garantia Judicial', DEFAULT_FILES, 'Lead de Garantia Gerado', 'Perfil Garantia Judicial', DEFAULT_STATUS_PRODUCT_GARANTIA, ),
                   ('Fiança Locatícia', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Fiança Locatícia', DEFAULT_FILES, 'Lead de Garantia Gerado', 'Perfil Fiança Locatícia', DEFAULT_STATUS_PRODUCT_GARANTIA, ),
                   )

DEFAULT_PROFILE_NAME = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
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

DEFAULT_PROFILE_PERMISSION = (('Perfil Parceiro Diretor', '1', '1', '1', ('0', '0', '0', '0'), '1', '1',
                               DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil Parceiro Supervisor', '1', '1', '1', ('0', '0', '0', '0'), '1', '1',
                               DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil Parceiro Gerente', '1', '1', '1', ('0', '0', '0', '0'), '1', '1',
                               DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil Parceiro Administrador', '1', '1', '1', ('1', '0', '0', '0'), '1', '1',
                               DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Administrador', '1', '1', '1', ('1', '1', '1', '1'), '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Gerencial', '0', '0', '1', ('0', '0', '0', '0'), '0', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Comercial', '1', '0', '1', ('0', '0', '0', '0'), '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Operacional', '1', '0', '1', ('0', '0', '0', '0'), '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Técnico Benefícios', '1', '0', '1', ('0', '0', '0', '0'), '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Técnico Garantia', '1', '0', '1', ('0', '0', '0', '0'), '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil GalCorr Financeiro', '1', '0', '1', ('0', '0', '0', '0'), '1', '1',
                               DEFAULT_PRODUCT_NAME_INSURANCE, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_STATUS, DEFAULT_FILES, DEFAULT_FILES, DEFAULT_PROFILE_NAME, ),
                              ('Perfil Tokio', '1', '1', '1', ('0', '0', '0', '0'), '1', '1',
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

        if Partner.objects.filter(id=2).exists():
            p = Partner.objects.get(id=2)
        else:
            s = Site(domain='galcorr', name='GalCorr')
            s.save()
            p = Partner(
                name='GalCorr',
                email='GalCorr@mail.com',
                cnpj='00.000.000.0000-00',
                site=s,
            )
            p.save()


        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", "admin", partner=p)

        if not User.objects.filter(username="demo").exists():
            u = User(username="demo", email="demo@demo.com", password="massificadodemo", partner=p)
            u.save()

        for status_name, level in DEFAULT_STATUS:
            if not Status.objects.filter(name=status_name).exists():
                st = Status(name=status_name, level=level)
                st.save()

        for status_name, level in DEFAULT_STATUS:
            if not StatusSee.objects.filter(name=status_name).exists():
                st = StatusSee(name=status_name, level=level)
                st.save()

        for status_name, level in DEFAULT_STATUS:
            if not StatusEdit.objects.filter(name=status_name).exists():
                st = StatusEdit(name=status_name, level=level)
                st.save()

        for status_name, level in DEFAULT_STATUS:
            if not StatusSet.objects.filter(name=status_name).exists():
                st = StatusSet(name=status_name, level=level)
                st.save()

        for status_name, level in DEFAULT_STATUS:
            if not StatusPermission.objects.filter(name=status_name).exists():
                st = StatusPermission(name=status_name, level=level)
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
        begin, profile, status_permitted in DEFAULT_PRODUCT:
            if not Product.objects.filter(name=product_name).exists():
                product = Product(
                    name=product_name,
                    introduction=introduction,
                    description=description,
                    declaration=declaration,
                    kind_person=kind,
                    insurance_company=InsuranceCompany.objects.get(name=insurance),
                    branch=Branch.objects.get(name=branch),
                    begin_status=Status.objects.get(name=begin),
                    profile=Profile.objects.get(name=profile)
                )

                product.save()
                for file in files:
                    product.file_type.add(FileType.objects.get(name=file))

                for permitted in status_permitted:
                    product.status_permission.add(Status.objects.get(name=permitted))

        for profile in DEFAULT_PROFILE_NAME:
            if not Profiles.objects.filter(name=profile).exists():
                per = Profiles(name=profile)
                per.save()

        for permission_name, menu_active_product, menu_active_dashboard, menu_active_production, menu_active_entries, menu_active_notification, menu_active_profile,\
                products_permission, status_see_permission, status_edit_permission, status_set_permission, filetype_see_permission, filetype_download_permission, profile_names_permission \
                in DEFAULT_PROFILE_PERMISSION:
            if not MassificadoGroups.objects.filter(name=permission_name).exists():
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

                for status_see_p_name, level in status_see_permission:
                     group.status_see.add(StatusSee.objects.get(name=status_see_p_name))

                for status_edit_p_name, level in status_edit_permission:
                    group.status_edit.add(StatusEdit.objects.get(name=status_edit_p_name))

                for status_set_p_name, level in status_set_permission:
                    group.status_set.add(StatusSet.objects.get(name=status_set_p_name))

                for filetype_see_p in filetype_see_permission:
                    group.filetype_see.add(FileTypeSee.objects.get(name=filetype_see_p))

                for filetype_download_p in filetype_download_permission:
                    group.filetype_download.add(FileTypeDownload.objects.get(name=filetype_download_p))

                for profile_names_p in profile_names_permission:
                    group.profiles.add(Profiles.objects.get(name=profile_names_p))
