#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views import generic
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# from django.views.generic.base import TemplateView
# from django.views.generic.list import ListView
from graphos.renderers import flot
from graphos.sources.model import ModelDataSource
from graphos.sources.model import SimpleDataSource
from models import Account
from models import Signal
from utils import wifi
from utils import wifi2

#import para o bokeh
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
# bokeh server
import numpy as np
from numpy import pi

from bokeh.client import push_session
from bokeh.driving import cosine
from bokeh.plotting import figure, curdoc


from bokeh.embed import autoload_server


class Index(generic.TemplateView):
    template_name = 'omf/index.html'


class ExpSF(generic.TemplateView):
    template_name = 'omf/experimentos.html'


class Exp1(generic.ListView):
    template_name = 'omf/experimento1_old.html'
    model = Signal

    def get_context_data(self, **kwargs):
        context = super(Exp1, self).get_context_data(**kwargs)
        queryset = Signal.objects.all()
        data_source = ModelDataSource(queryset, fields=['id', 'signal'])
        chart = flot.LineChart(data_source, options={'title':  "Sales Growth"})
        context['chart'] = chart
        return context


def scan(request):
    #wifi.main()
    wifi2.main()
    #return render(request, 'omf/experimento1_old.html', {'chart': chart})
    return HttpResponseRedirect(reverse('omf:exp1'))

# class Teste(generic.View):
#     template_name = 'omf/teste.html'
#     model = Signal
#
#     def get(self, request):
#
#         x = Signal.objects.values_list('time', flat=True).order_by('id')
#         y = Signal.objects.values_list('signal', flat=True).order_by('id')
#         #x = (5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5)
#         plot = figure(title="simple line example", x_axis_label='x', y_axis_label='y', x_range=(0, 10))
#         plot.line(x, y, legend="Temp.", line_width=2)
#
#         script, div = components(plot, CDN)
#
#         return render(request, self.template_name, {"the_script": script, "the_div": div})


class Teste(generic.View):
    template_name = 'omf/teste.html'
    model = Signal

    def get(self, request):

        # x = np.linspace(0, 4 * pi, 80)
        # y = np.sin(x)
        #
        # p = figure()
        # r1 = p.line([0, 4 * pi], [-1, 1], color="firebrick")
        # r2 = p.line(x, y, color="navy", line_width=4)
        #
        # session = push_session(curdoc())
        #
        # @cosine(w=0.03)
        # def update(step):
        #     # updating a single column of the the *same length* is OK
        #     r2.data_source.data["y"] = y * step
        #     r2.glyph.line_alpha = 1 - 0.8 * abs(step)
        #
        # curdoc().add_periodic_callback(update(), 50)
        #
        # session.loop_until_closed()  # run forever
        #
        # script = autoload_server(p, session_id=session.id)
        script = autoload_server(model=None, app_path='/app')

        return render(request, self.template_name, {"the_div": script})


class Experimento1(generic.View):
    template_name = 'omf/experimento1.html'
    model = Signal

    def get(self, request):
        script = autoload_server(model=None, app_path='/wireless')
        return render(request, self.template_name, {"the_div": script})

class Experimento2(generic.View):
    template_name = 'omf/experimento2.html'
    model = Signal

    def get(self, request):
        script = autoload_server(model=None, app_path='/wireless2')
        return render(request, self.template_name, {"the_div": script})

class TrainControl(generic.TemplateView):
    template_name = 'omf/trainControl.html'