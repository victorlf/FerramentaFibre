#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views import generic
from utils.reservarNos import reserva #reserva de nós
from bokeh.embed import autoload_server #ler aplicação do bokeh server

import numpy as np


class Index(generic.TemplateView):
    template_name = 'wired/index.html'

class Reserva(generic.View):
    template_name = 'wired/reserva.html'

    numbers = list()
    for number in np.arange(0.5, 4.5, 0.5):
        numbers.append('%g'%number)

    def get(self, request):
        return render(request, self.template_name, {"range1": range(0, 10), "range2": range(10, 24), "range3": self.numbers})

def reservar(request):
    #template_name = 'wired/reserva.html'
    data = request.POST['data']
    hora = request.POST['hora']
    minuto = request.POST['minuto']
    duracao = request.POST['duracao']

    univ = request.POST['universidade']

    nodes = list()


    for i in range(1, 9):
        node = univ + 'node' + str(i)
        if node in request.POST: #evita erros
            nodes.append(request.POST[node])

    try:
        reserva(univ, data, hora, minuto, duracao, nodes)
    except ValueError:
        messages.warning(request, 'Um ou mais nós não estão disponíveis para esse dia e horário.')
        #return render(request, template_name, {"range1": range(0, 10), "range2": range(10, 24), "range3": np.arange(0.5, 4.5, 0.5)})
        return HttpResponseRedirect(reverse('wired:reserva'))
    #return render(request, template_name, {"range1": range(0, 10), "range2": range(10, 24), "range3": np.arange(0.5, 4.5, 0.5)})
    messages.success(request, 'feita.')
    return HttpResponseRedirect(reverse('wired:reserva'))

class WirelessExperiment(generic.View):
    template_name = 'wired/wirelessExperiment.html'

    def get(self, request):
        UFGscript = autoload_server(model=None, app_path='/UFGwireless2')
        UFFscript = autoload_server(model=None, app_path='/UFFwireless2')
        return render(request, self.template_name, {"UFGthe_div": UFGscript, "UFFthe_div": UFFscript})

class PowerControlExperiment(generic.View):
    template_name = 'wired/powerControlExperiment.html'

    def get(self, request):
        script = autoload_server(model=None, app_path='/UFGpowerControl')
        return render(request, self.template_name, {"the_div": script})

class TcpBitrateExperiment(generic.View):
    template_name = 'wired/tcpBitrateExperiment.html'

    def get(self, request):
        script = autoload_server(model=None, app_path='/UFGtcpBitrate')
        return render(request, self.template_name, {"the_div": script})