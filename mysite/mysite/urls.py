# coding=utf-8
"""mysite URL Configuration

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

from django.conf.urls import include, url
from django.contrib import admin

import views

urlpatterns = [
    #url(r'^chat/', include('chat.urls')),
    url(r'^', include('base.urls')),
    url(r'^omf/', include('omf.urls')),  # requisição que começar com 'omf' será redirecionado para o urls do wireless 'omf'
    url(r'^wired/', include('wired.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]



