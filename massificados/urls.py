# -*- coding: utf-8 -*-
"""massificados URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.defaults import page_not_found
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from core.views import IndexView, EntriesView
from sale.views import ProductionView, CreateBuyerView, EditBuyerView, ProposePDF, user_cnpj, upload_media
from user_account.views import (EntriesProfilesView, EntriesUsersView, EntrieUserNewView, EntrieUserEditView,
                                NotificationsView)
from user_groups.views import EntrieProfileNewView, EntrieProfileEditView

from partner.views import SacsListView


import notifications.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^sac/', SacsListView.as_view(), name='sac'),

    url(r'^entries/$', EntriesView.as_view(), name='entries'),

    url(r'^entries/users/$', EntriesUsersView.as_view(), name='entries-users'),
    url(r'^entries/users/new/', EntrieUserNewView.as_view(), name='entries-users-new'),
    url(r'^entries/users/(?P<pk>[0-9]+)/$', EntrieUserEditView.as_view(), name='entries-users-edit'),

    url(r'^entries/profiles/$', EntriesProfilesView.as_view(), name='entries-profiles'),
    url(r'^entries/profiles/new/$', EntrieProfileNewView.as_view(), name='entries-profiles-new'),
    url(r'^entries/profiles/(?P<pk>[0-9]+)/$', EntrieProfileEditView.as_view(), name='entries-profiles-edit'),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^product/(?P<productpk>[0-9]+)/buyer/$', CreateBuyerView.as_view(), name='product-new-buyer'),
    url(r'^product/(?P<productpk>[0-9]+)/buyer/(?P<pk>[0-9]+)$', EditBuyerView.as_view(), name='product-edit-buyer'),

    url(r'^production/$', ProductionView.as_view(), name='production'),

    url(r'^404/$', page_not_found, name='error_404'),

    url(r'^notifications/$', NotificationsView.as_view(), name="notifications"),

    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications-api')),

    url(r'^propose/(?P<salepk>[0-9]+)/$', ProposePDF.as_view(), name='propose-pdf'),

    # api
    url(r'^api/user_cnpj', user_cnpj),
    url(r'^api/upload_media', upload_media)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^rosetta/', include('rosetta.urls')),
    ]
