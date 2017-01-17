from django.conf.urls import url

from . import views

app_name = 'base'

urlpatterns = [
    #/base
    url(r'^$', views.Index.as_view(), name='index'),
]