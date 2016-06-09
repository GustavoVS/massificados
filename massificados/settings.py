# -*- coding: utf-8 -*-
"""
Django settings for massificados project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

THEMES_DIR = os.path.join(BASE_DIR, 'themes')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used inm production secret!
SECRET_KEY = 'rjy@i6@99qth)#8o!)z!hjk^mi@l7d6$#gfa_pu!91@i&2jtbf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = [
#     '*',
# ]
ALLOWED_HOSTS = ['localhost']

AUTH_USER_MODEL = 'user_account.MassificadoUser'

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Massificados
    'user_account',
    'user_groups',
    'partner',
    'product',
    'sale',
    'core',
    'status_emails',
    # 3rd
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rosetta',
    'django_extensions',
    'notifications',
    'bootstrap3',
    'rest_framework',
    'storages',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'massificados.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(THEMES_DIR, 'default', 'templates'),
            os.path.join(THEMES_DIR),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',

            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'massificados.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
if 'RDS_DB_NAME' in os.environ:
    # DEBUG = False
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'massificados',
            'USER': 'massificados',
            'PASSWORD': 'minhapicapreta',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'pt-br'

LANGUAGES = (
    ('pt-br', _('Brazilian Portuguese')),
    ('en-us', _('English')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# STATIC_ROOT = os.path.join(BASE_DIR, '..', 'www', 'static')
STATIC_ROOT = 'static'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'www', 'media')

STATICFILES_DIRS = (
    os.path.join(THEMES_DIR, 'default', 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",
                           "allauth.account.auth_backends.AuthenticationBackend")

ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_ADAPTER = 'mysite.account_adapter.NoNewUsersAccountAdapter'
ACCOUNT_ADAPTER = 'user_account.adapter.NoSignUp'


if DEBUG:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1', )

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

BOOTSTRAP3 = {
    'required_css_class': 'form-required',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'galcorrmassificados@gmail.com'
EMAIL_HOST_PASSWORD = '123ABC#456'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

NOTIFICATION_FROM_EMAIL = 'noreply@lightstudios.com.br'


AWS_STORAGE_BUCKET_NAME = 'massificados-media'
AWS_ACCESS_KEY_ID = 'AKIAIC7XGUQ2OFZ62S7Q'
AWS_SECRET_ACCESS_KEY = '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'

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'massificados.custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

DEFAULT_FILE_STORAGE = 'massificados.custom_storages.MediaStorage'
