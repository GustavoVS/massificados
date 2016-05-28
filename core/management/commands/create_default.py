# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from partner.models import Partner
from product.models import Status, FileType, InsuranceCompany, Branch, Product, Profile, ActionStatus
from user_account.models import MassificadoUser
from user_groups.models import MassificadoGroups
from status_emails.models import ActionStatusEmails, ActionStatusEmailsUsers

User = get_user_model()

DEFAULT_STATUS = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

# Produtos permitidos no perfil de acesso
DEFAULT_PRODUCT_NAME_GALCORR = (
    'Vida', 'Vida Global', 'Acidentes Pessoais', 'Garantia Tradicional',
    'Garantia Judicial', 'Fiança Locatícia', 'Saúde',)
DEFAULT_PRODUCT_NAME_PARTNER = (
    'Vida', 'Vida Global', 'Acidentes Pessoais', 'Garantia Tradicional',
    'Garantia Judicial', 'Fiança Locatícia', 'Saúde',)
DEFAULT_PRODUCT_NAME_TOKIO = ('Vida', 'Vida Global', 'Acidentes Pessoais',)
DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS = ('Saúde',)
DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA = ('Garantia Tradicional', 'Garantia Judicial', 'Fiança Locatícia',)

# Status x Perfil
DEFAULT_STATUS_PROFILE_TOKIO_SEE = (('Proposta Gerada', 1), ('Boleto Gerado', 2), ('Apólice Gerada', 3),)

DEFAULT_STATUS_PROFILE_TOKIO_EDIT = (('Proposta Gerada', 1), ('Boleto Gerado', 2), ('Apólice Gerada', 3),)

DEFAULT_STATUS_PROFILE_TOKIO_SET = (('Boleto Gerado', 2), ('Apólice Gerada', 3),)

DEFAULT_STATUS_PROFILE_PARTNER_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_PARTNER_EDIT = (
    ('Lead de Garantia Gerado', 2), ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Lead de Benefícios Gerado', 2), ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Proposta Gerada', 1),
)

DEFAULT_STATUS_PROFILE_PARTNER_SET = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2),
    ('Proposta Gerada', 1),
)

DEFAULT_STATUS_PROFILE_GALCORR_ADM_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_ADM_EDIT = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_ADM_SET = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_GER_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_GER_EDIT = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_GER_SET = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_COM_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_COM_EDIT = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2)
)

DEFAULT_STATUS_PROFILE_GALCORR_COM_SET = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),

    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),

    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Apólice Cancelada', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_OPE_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_OPE_EDIT = (
    ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),

    ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),

    ('Proposta Gerada', 1),
)

DEFAULT_STATUS_PROFILE_GALCORR_OPE_SET = (
    ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),

    ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),

    ('Proposta Gerada', 1), ('Apólice Cancelada', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECB_SEE = (
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2),
    ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECB_EDIT = (
    ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECB_SET = (
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECG_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2),
    ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECG_EDIT = (
    ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECG_SET = (
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_FIN_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2),
    ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2),
    ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2),
    ('Apólice Gerada', 3), ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_FIN_EDIT = (
     ('Apólice Gerada', 3), ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_FIN_SET = (
     ('Repasse Pago', 4),
)

# Produtos x Status Possíveis

DEFAULT_STATUS_PRODUCT_TOKIO = (('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2),
    ('Apólice Gerada', 3), ('Apólice Cancelada', 4), ('Repasse Pago', 4),)

DEFAULT_STATUS_PRODUCT_GARANTIA = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
)

DEFAULT_STATUS_PRODUCT_BENEFICIOS = (
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
)

# Email x Status x Responsável x Produto

DEFAULT_STATUS_PRODUCT_TOKIO_EMAIL = (
    ('Proposta Gerada', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('{Seguradora}', 'inc'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Proposta Cancelada', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('{Seguradora}', 'inc'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Boleto Gerado', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('{Seguradora}', 'inc'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Apólice Gerada', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('{Seguradora}', 'inc'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('lucia.moraes@galcorr.com.br', 'usr'),),),
    ('Apólice Cancelada', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('{Seguradora}', 'inc'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('lucia.moraes@galcorr.com.br', 'usr'),),),
    ('Repasse Pago', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('flavio.saraiva@galcorr.com.br', 'usr',),),),)


DEFAULT_STATUS_PRODUCT_GARANTIA_EMAIL = (
    ('Lead de Garantia Gerado', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('{Gerente}', 'own'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Lead de Garantia Cancelado', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('{Gerente}', 'own'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Solicitação de Cotação de Garantia', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',), ('rafael.nunes@comercialseguros.com.br', 'usr'),),),
    ('Cotação de Garantia Gerada', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',), ('rafael.nunes@comercialseguros.com.br', 'usr'),),),
    ('Cotação de Garantia não Gerada - Faltam documentos', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',), ('rafael.nunes@comercialseguros.com.br', 'usr'),),),
    ('Cotação de Garantia Negada', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('rafael.nunes@comercialseguros.com.br', 'usr'), ('{Gerente}', 'own'),),),
    ('Cotação de Garantia Aprovada', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('rafael.nunes@comercialseguros.com.br', 'usr'), ('{Gerente}', 'own'),),),
)

DEFAULT_STATUS_PRODUCT_BENEFICIOS_EMAIL = (
    ('Lead de Benefícios Gerado', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('{Gerente}', 'own'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Lead de Benefícios Cancelado', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('{Gerente}', 'own'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Solicitação de Cotação de Benefícios', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',), ('adriano.telles@galcorr.com.br', 'usr'),),),
    ('Cotação de Benefícios Gerada', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',), ('adriano.telles@galcorr.com.br', 'usr'),),),
    ('Cotação de Benefícios não Gerada - Faltam documentos', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('adriano.telles@galcorr.com.br', 'usr'), ('rafael.nunes@comercialseguros.com.br', 'usr'),),),
    ('Cotação de Benefícios Negada', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('adriano.telles@galcorr.com.br', 'usr'), ('{Gerente}', 'own'),),),
    ('Cotação de Benefícios Aprovada', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('adriano.telles@galcorr.com.br', 'usr'), ('{Gerente}', 'own'),),),
)

# Arquivos
DEFAULT_FILES = (
    'Proposta de Endosso', 'Proposta de Apólice', 'Endosso', 'Apólice',
    'Boleto de Apólice', 'Boleto de Endosso', 'Boleto de Apólice 2ª via', 'Boleto de Endosso 2ª via',
    'Demonstrações financeiras de 2013 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2014 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2015 (assinadas e/ou auditadas)',
    'Contrato/Estatuto Social e ata de eleição da última diretoria',
    'Fichas cadastrais preenchidas e assinadas',
    'Apresentação Institucional',
)

DEFAULT_FILES_GALCORR = (
    'Proposta de Endosso', 'Proposta de Apólice', 'Endosso', 'Apólice',
    'Demonstrações financeiras de 2013 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2014 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2015 (assinadas e/ou auditadas)',
    'Contrato/Estatuto Social e ata de eleição da última diretoria',
    'Fichas cadastrais preenchidas e assinadas',
    'Apresentação Institucional',
)

DEFAULT_FILES_PARTNER = (
    'Demonstrações financeiras de 2013 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2014 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2015 (assinadas e/ou auditadas)',
    'Contrato/Estatuto Social e ata de eleição da última diretoria',
    'Fichas cadastrais preenchidas e assinadas',
    'Apresentação Institucional',
)

DEFAULT_FILES_TOKIO = (
    'Proposta de Endosso', 'Proposta de Apólice', 'Endosso', 'Apólice',
    'Boleto de Apólice', 'Boleto de Endosso', 'Boleto de Apólice 2ª via', 'Boleto de Endosso 2ª via',
)

DEFAULT_FILES_GARANTIA = (
    'Demonstrações financeiras de 2013 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2014 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2015 (assinadas e/ou auditadas)',
    'Contrato/Estatuto Social e ata de eleição da última diretoria',
    'Fichas cadastrais preenchidas e assinadas',
    'Apresentação Institucional',
)

DEFAULT_FILES_BENEFICIOS = (
    'Demonstrações financeiras de 2013 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2014 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2015 (assinadas e/ou auditadas)',
    'Contrato/Estatuto Social e ata de eleição da última diretoria',
    'Fichas cadastrais preenchidas e assinadas',
    'Apresentação Institucional',
)

DEFAULT_INSURANCE = (('Tokio', '123456', 'r.cabral.n@gmail.com',), ('GalCorr', '000000', 'r.cabral.n@gmail.com',),)

DEFAULT_BRANCH = (
    'Vida', 'Acidentes Pessoais',
    'Garantia Tradicional', 'Garantia Judicial', 'Fiança Locatícia', 'Saúde',)

DEFAULT_PROFILE = (
    'Perfil Vida', 'Perfil Vida Global', 'Perfil Acidentes Pessoais', 'Perfil Garantia Tradicional',
    'Perfil Garantia Judicial', 'Perfil Fiança Locatícia', 'Perfil Saúde',)

# Produtos para serem incluídos
DEFAULT_PRODUCT = (
    ('Vida', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Vida',
        DEFAULT_FILES_TOKIO,
        'Proposta Gerada', 'Perfil Vida', DEFAULT_STATUS_PRODUCT_TOKIO,),
    ('Vida Global', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Vida',
         DEFAULT_FILES_TOKIO,
        'Proposta Gerada', 'Perfil Vida Global', DEFAULT_STATUS_PRODUCT_TOKIO,),
    ('Acidentes Pessoais', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Acidentes Pessoais',
        DEFAULT_FILES_TOKIO,
        'Proposta Gerada', 'Perfil Acidentes Pessoais', DEFAULT_STATUS_PRODUCT_TOKIO,),
    ('Garantia Tradicional', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Garantia Tradicional',
        DEFAULT_FILES_GARANTIA,
        'Lead de Garantia Gerado', 'Perfil Garantia Tradicional', DEFAULT_STATUS_PRODUCT_GARANTIA,),
    ('Garantia Judicial', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Garantia Judicial',
         DEFAULT_FILES_GARANTIA,
        'Lead de Garantia Gerado', 'Perfil Garantia Judicial', DEFAULT_STATUS_PRODUCT_GARANTIA,),
    ('Fiança Locatícia', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Fiança Locatícia',
     DEFAULT_FILES_GARANTIA,
    'Lead de Garantia Gerado', 'Perfil Fiança Locatícia', DEFAULT_STATUS_PRODUCT_GARANTIA,),
    ('Saúde', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Saúde',
     DEFAULT_FILES_BENEFICIOS,
    'Lead de Benefícios Gerado', 'Perfil Saúde', DEFAULT_STATUS_PRODUCT_BENEFICIOS,),
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

PROFILE_NAME_PARTNER_ADM = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
)

PROFILE_NAME_PARTNER_DIR = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
)

PROFILE_NAME_PARTNER_SUP = (
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
)

PROFILE_NAME_PARTNER_GER = (
    'Perfil Parceiro Gerente',
)

PROFILE_NAME_TOKIO = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
)


PROFILE_NAME_GALCORR_ADM = (
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

PROFILE_NAME_GALCORR_GER = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Gerencial',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
    'Perfil GalCorr Técnico Garantia',
    'Perfil GalCorr Financeiro',
    'Perfil Tokio'
)

PROFILE_NAME_GALCORR_COM = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
    'Perfil GalCorr Técnico Garantia',
    'Perfil GalCorr Financeiro',
    'Perfil Tokio'
)

PROFILE_NAME_GALCORR_OPE = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
    'Perfil GalCorr Técnico Garantia',
    'Perfil GalCorr Financeiro',
)

PROFILE_NAME_GALCORR_TECB = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
)

PROFILE_NAME_GALCORR_TECG = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Garantia',
)

PROFILE_NAME_GALCORR_FIN = (
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

DEFAULT_PROFILE_PERMISSION = (
    ('Perfil Parceiro Diretor', 1, 1, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS_PROFILE_PARTNER_SEE, DEFAULT_STATUS_PROFILE_PARTNER_EDIT,
     DEFAULT_STATUS_PROFILE_PARTNER_SET, DEFAULT_FILES_PARTNER, DEFAULT_FILES_PARTNER, PROFILE_NAME_PARTNER_DIR,),
    ('Perfil Parceiro Supervisor', 1, 1, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS_PROFILE_PARTNER_SEE, DEFAULT_STATUS_PROFILE_PARTNER_EDIT,
     DEFAULT_STATUS_PROFILE_PARTNER_SET, DEFAULT_FILES_PARTNER, DEFAULT_FILES_PARTNER, PROFILE_NAME_PARTNER_SUP,),
    ('Perfil Parceiro Gerente', 1, 1, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS_PROFILE_PARTNER_SEE, DEFAULT_STATUS_PROFILE_PARTNER_EDIT,
     DEFAULT_STATUS_PROFILE_PARTNER_SET, DEFAULT_FILES_PARTNER, DEFAULT_FILES_PARTNER, PROFILE_NAME_PARTNER_GER,),
    ('Perfil Parceiro Administrador', 1, 1, 1, 1, (1, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS_PROFILE_PARTNER_SEE, DEFAULT_STATUS_PROFILE_PARTNER_EDIT,
     DEFAULT_STATUS_PROFILE_PARTNER_SET, DEFAULT_FILES_PARTNER, DEFAULT_FILES_PARTNER, PROFILE_NAME_PARTNER_ADM,),
    ('Perfil GalCorr Administrador', 1, 1, 1, 1, (1, 1, 1, 1), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR, DEFAULT_STATUS_PROFILE_GALCORR_ADM_SEE, DEFAULT_STATUS_PROFILE_GALCORR_ADM_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_ADM_SET, DEFAULT_FILES_GALCORR, DEFAULT_FILES_GALCORR, PROFILE_NAME_GALCORR_ADM,),
    ('Perfil GalCorr Gerencial', 0, 0, 1, 0, (0, 0, 0, 0), 0, 1,
     DEFAULT_PRODUCT_NAME_GALCORR, DEFAULT_STATUS_PROFILE_GALCORR_GER_SEE, DEFAULT_STATUS_PROFILE_GALCORR_GER_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_GER_SET, DEFAULT_FILES_GALCORR, DEFAULT_FILES_GALCORR, PROFILE_NAME_GALCORR_GER,),
    ('Perfil GalCorr Comercial', 1, 0, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR, DEFAULT_STATUS_PROFILE_GALCORR_COM_SEE, DEFAULT_STATUS_PROFILE_GALCORR_COM_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_COM_SET, DEFAULT_FILES_GALCORR, DEFAULT_FILES_GALCORR, PROFILE_NAME_GALCORR_COM,),
    ('Perfil GalCorr Operacional', 1, 0, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR, DEFAULT_STATUS_PROFILE_GALCORR_OPE_SEE, DEFAULT_STATUS_PROFILE_GALCORR_OPE_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_OPE_SET, DEFAULT_FILES_GALCORR, DEFAULT_FILES_GALCORR, PROFILE_NAME_GALCORR_OPE,),
    ('Perfil GalCorr Técnico Benefícios', 1, 0, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS, DEFAULT_STATUS_PROFILE_GALCORR_TECB_SEE,
     DEFAULT_STATUS_PROFILE_GALCORR_TECB_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_TECB_SET, DEFAULT_FILES_BENEFICIOS, DEFAULT_FILES_BENEFICIOS,
     PROFILE_NAME_GALCORR_TECB,),
    ('Perfil GalCorr Técnico Garantia', 1, 0, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA, DEFAULT_STATUS_PROFILE_GALCORR_TECG_SEE,
     DEFAULT_STATUS_PROFILE_GALCORR_TECG_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_TECG_SET, DEFAULT_FILES_GARANTIA, DEFAULT_FILES_GARANTIA,
     PROFILE_NAME_GALCORR_TECG,),
    ('Perfil GalCorr Financeiro', 1, 0, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR, DEFAULT_STATUS_PROFILE_GALCORR_FIN_SEE, DEFAULT_STATUS_PROFILE_GALCORR_FIN_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_FIN_SET, DEFAULT_FILES_GALCORR, DEFAULT_FILES_GALCORR, PROFILE_NAME_GALCORR_FIN,),
    ('Perfil Tokio', 1, 1, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_TOKIO, DEFAULT_STATUS_PROFILE_TOKIO_SEE, DEFAULT_STATUS_PROFILE_TOKIO_EDIT,
     DEFAULT_STATUS_PROFILE_TOKIO_SET, DEFAULT_FILES_TOKIO, DEFAULT_FILES_TOKIO, PROFILE_NAME_TOKIO,),)


USERS = (
    ('Perfil Parceiro Diretor', '123', 'Sofisa', 'DiretorSofisa@mail.com', 'DiretorSofisa',),
    ('Perfil Parceiro Supervisor', '123', 'Sofisa', 'SupervisorSofisa@mail.com', 'SupervisorSofisa',),
    ('Perfil Parceiro Gerente', '123', 'Sofisa', 'GerenteSofisa@mail.com', 'GerenteSofisa',),
    ('Perfil Parceiro Administrador', '123', 'Sofisa', 'AdministradorSofisa@mail.com', 'AdministradorSofisa',),
    ('Perfil GalCorr Administrador', '123', 'GalCorr', 'fabiano.costa@galcorr.com.br', 'AdministradorGalCorr',),
    ('Perfil GalCorr Gerencial', '123', 'GalCorr', 'GerenteGalCorr@mail.com', 'GerenteGalCorr',),
    ('Perfil GalCorr Comercial', '123', 'GalCorr', 'flavio.saraiva@galcorr.com.br', 'ComercialGalCorr',),
    ('Perfil GalCorr Operacional', '123', 'GalCorr', 'lucia.moraes@galcorr.com.br', 'OperacionalGalCorr',),
    ('Perfil GalCorr Técnico Benefícios', '123', 'GalCorr', 'adriano.telles@galcorr.com.br', 'TecnicoBeneficiosGalCorr',),
    ('Perfil GalCorr Técnico Garantia', '123', 'GalCorr', 'rafael.nunes@comercialseguros.com.br', 'TecnicoGarantiaGalCorr',),
    ('Perfil GalCorr Financeiro', '123', 'GalCorr', 'FinanceiroGalCorr@mail.com', 'FinanceiroGalCorr',),
    ('Perfil Tokio', '123', 'GalCorr', 'r.cabral.n@gmail.com', 'TokioMarine',),
)


class Command(BaseCommand):
    help = 'Cria dados padrões para o início da aplicação'

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

        if Partner.objects.filter(id=3).exists():
            p = Partner.objects.get(id=3)
        else:
            s = Site(domain='tokio', name='Tokio')
            s.save()
            p = Partner(
                name='Tokio',
                email='Tokio@mail.com',
                cnpj='00.000.000.0000-00',
                site=s,
            )
            p.save()

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", "admin", partner=p)

        if not User.objects.filter(username="demo").exists():
            u = User(username="demo", email="demo@demo.com", password="massificadodemo", partner=p)
            u.save()

        for user_profile, user_password, user_partner, user_email, user_name in USERS:
            if not MassificadoUser.objects.filter(email=user_email).exists():
                user = MassificadoUser(username=user_name,
                                       email=user_email,
                                       password=user_password,
                                       partner=Partner.objects.get(name=user_partner))
                user.save()

        for status_name, level in DEFAULT_STATUS:
            if not Status.objects.filter(name=status_name).exists():
                st = Status(name=status_name, level=level)
                st.save()

        for file_name in DEFAULT_FILES:
            if not FileType.objects.filter(name=file_name).exists():
                fl = FileType(name=file_name)
                fl.save()

        for file_name in DEFAULT_FILES:
            if not FileType.objects.filter(name=file_name).exists():
                fl = FileType(name=file_name)
                fl.save()

        for file_name in DEFAULT_FILES:
            if not FileType.objects.filter(name=file_name).exists():
                fl = FileType(name=file_name)
                fl.save()

        for cia, susep, email in DEFAULT_INSURANCE:
            if not InsuranceCompany.objects.filter(name=cia).exists():
                insurance_company = InsuranceCompany(name=cia, susep=susep, email=email)
                insurance_company.save()

        for branch_name in DEFAULT_BRANCH:
            if not Branch.objects.filter(name=branch_name).exists():
                branch = Branch(name=branch_name)
                branch.save()

        for profile_name in DEFAULT_PROFILE:
            if not Profile.objects.filter(name=profile_name).exists():
                pe = Profile(name=profile_name)
                pe.save()

        # for profile in DEFAULT_PROFILE_NAME:
        #     if not MassificadoGroups.objects.filter(name=profile).exists():
        #         per = MassificadoGroups(name=profile)
        #         per.save()

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

                for status_p, level in status_permitted:
                    product.status_permission.add(Status.objects.get(name=status_p))

                for status_p, lever in status_permitted:
                    action_st = ActionStatus(
                             product=product,
                             status=Status.objects.get(name=status_p))
                    action_st.save()
                    for st, products_emails, emails in DEFAULT_STATUS_PRODUCT_TOKIO_EMAIL:
                        if st == status_p:
                            for product_emails in products_emails:
                                if product_emails == product_name:
                                    for email, type in emails:
                                        action_st_email = ActionStatusEmails(action_status=action_st, action_email=type)
                                        action_st_email.save()
                                        if type == 'usr':
                                            if User.objects.filter(email=email).exists():
                                                action_st_email_user = ActionStatusEmailsUsers(
                                                    action_status_email=action_st_email,
                                                    user=User.objects.get(email=email))
                                                action_st_email_user.save()

                    for st, products_emails, emails in DEFAULT_STATUS_PRODUCT_BENEFICIOS_EMAIL:
                        if st == status_p:
                            for product_emails in products_emails:
                                if product_emails == product_name:
                                    for email, type in emails:
                                        action_st_email = ActionStatusEmails(action_status=action_st, action_email=type)
                                        action_st_email.save()
                                        if type == 'usr':
                                            if User.objects.filter(email=email).exists():
                                                action_st_email_user = ActionStatusEmailsUsers(
                                                    action_status_email=action_st_email,
                                                    user=User.objects.get(email=email))
                                                action_st_email_user.save()

                    for st, products_emails, emails in DEFAULT_STATUS_PRODUCT_GARANTIA_EMAIL:
                        if st == status_p:
                            for product_emails in products_emails:
                                if product_emails == product_name:
                                    for email, type in emails:
                                        action_st_email = ActionStatusEmails(action_status=action_st, action_email=type)
                                        action_st_email.save()
                                        if type == 'usr':
                                            if User.objects.filter(email=email).exists():
                                                action_st_email_user = ActionStatusEmailsUsers(
                                                    action_status_email=action_st_email,
                                                    user=User.objects.get(email=email))
                                                action_st_email_user.save()

        for permission_name, menu_active_product, menu_active_dashboard, menu_active_production, menu_active_entries,\
            menu_active_entries_detail, menu_active_notification, menu_active_profile, products_permission,\
            status_see_permission, status_edit_permission, status_set_permission, filetype_see_permission,\
            filetype_download_permission, profile_names_permission in DEFAULT_PROFILE_PERMISSION:

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
                group.menu_entries_users = menu_active_entries_detail[0]
                group.menu_entries_profiles = menu_active_entries_detail[1]
                group.menu_entries_partners = menu_active_entries_detail[2]
                group.menu_entries_products = menu_active_entries_detail[3]

                group.save()

        for permission_name, menu_active_product, menu_active_dashboard, menu_active_production, menu_active_entries,\
            menu_active_entries_detail, menu_active_notification, menu_active_profile, products_permission,\
            status_see_permission, status_edit_permission, status_set_permission, filetype_see_permission,\
            filetype_download_permission, profile_names_permission in DEFAULT_PROFILE_PERMISSION:

                if  MassificadoGroups.objects.filter(name=permission_name).exists():
                    group = MassificadoGroups.objects.get(name=permission_name)

                    for products_p in products_permission:
                        group.product.add(Product.objects.get(name=products_p))

                    for status_see_p_name, level in status_see_permission:
                         group.status_see.add(Status.objects.get(name=status_see_p_name))

                    for status_edit_p_name, level in status_edit_permission:
                        group.status_edit.add(Status.objects.get(name=status_edit_p_name))

                    for status_set_p_name, level in status_set_permission:
                        group.status_set.add(Status.objects.get(name=status_set_p_name))

                    for filetype_see_p in filetype_see_permission:
                        group.filetype_see.add(FileType.objects.get(name=filetype_see_p))

                    for filetype_download_p in filetype_download_permission:
                        group.filetype_download.add(FileType.objects.get(name=filetype_download_p))

                    for profile_names_p in profile_names_permission:
                        group.profiles.add(MassificadoGroups.objects.get(name=profile_names_p))

        for user_profile, user_password, user_partner, user_email, user_name in USERS:
                user = MassificadoUser.objects.get(email=user_email)
                user.set_password('galcorr')
                user.group_permissions = MassificadoGroups.objects.get(name=user_profile)
                user.save()
