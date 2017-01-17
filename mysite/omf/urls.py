from django.conf.urls import url

from . import views

app_name = 'omf'

urlpatterns = [
    #/omf
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^experimentos/$', views.ExpSF.as_view(), name='experimentos'),
    url(r'^exp1/$', views.Exp1.as_view(), name='exp1'),
    url(r'^scan/$', views.scan, name='scan'),
    url(r'^teste/$', views.Teste.as_view(), name='teste'),
    url(r'^experimento1/$', views.Experimento1.as_view(), name='experimento1'),
    url(r'^experimento2/$', views.Experimento2.as_view(), name='experimento2'),
    url(r'^trainControl/$', views.TrainControl.as_view(), name='trainControl'),
]