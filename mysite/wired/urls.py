from django.conf.urls import url

from . import views

app_name = 'wired'

urlpatterns = [
    #/wired
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^reserva/$', views.Reserva.as_view(), name='reserva'),
    url(r'^reservando/$', views.reservar, name='reservando'),
    url(r'^nosfixos/$', views.WirelessExperiment.as_view(), name='wirelessExperiment'),
    url(r'^nosfixosPowerControl/$', views.PowerControlExperiment.as_view(), name='powerControlExperiment'),
    url(r'^nosfixosTcpBitrate/$', views.TcpBitrateExperiment.as_view(), name='tcpBitrateExperiment'),
]
