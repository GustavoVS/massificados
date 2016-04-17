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
from django.conf.urls import url, include
from django.contrib import admin
from core.views import IndexView, EntriesView
from user_account.views import EntriesProfilesView, EntriesUsersView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^sac/', EntriesView.as_view(), name='sac'),

    url(r'^entries/$', EntriesView.as_view(), name='entries'),
    url(r'^entries/users/$', EntriesUsersView.as_view(), name='entries_users'),
    url(r'^entries/profiles/$', EntriesProfilesView.as_view(), name='entries_profiles'),


    url(r'^accounts/', include('allauth.urls')),

]
