#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Button
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

import sqlite3

source = ColumnDataSource(dict(x=[], y=[], y1=[]))
sourceCong = ColumnDataSource(dict(x=[], y3=[]))
sourceRtt = ColumnDataSource(dict(x=[], y4=[]))

TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

fig = Figure(tools=TOOLS, plot_width=800, title="Resultado", x_axis_type="datetime")
figCong = Figure(tools=TOOLS, plot_width=800, title="Congestionamento TCP", x_axis_type="datetime")
figRtt = Figure(tools=TOOLS, plot_width=800, title="RTT", x_axis_type="datetime")

fig.line(source=source, x='x', y='y', legend="Server Input",line_width=2, color='blue', alpha=0.5)
fig.line(source=source, x='x', y='y1', legend="Client Output",line_width=2, color='red', alpha=0.5)

figCong.line(source=sourceCong, x='x', y='y3', legend="RSSI",line_width=2, color='yellow', alpha=0.5)

figRtt.line(source=sourceRtt, x='x', y='y3', legend="RSSI",line_width=2, color='green', alpha=0.5)

# Legendas do Gráfico
fig.yaxis.axis_label = "Mbps"
fig.xaxis.axis_label = "Segundos"
fig.legend.location = "bottom_left"
# Legendas do Gráfico
figCong.yaxis.axis_label = "Packets"
figCong.xaxis.axis_label = "Segundos"
figCong.legend.location = "bottom_left"
# Legendas do Gráfico
figRtt.yaxis.axis_label = "ms"
figRtt.xaxis.axis_label = "Segundos"
figRtt.legend.location = "bottom_left"

ct = 0
sine_sum = 0
sine = list()
tempo = list()
sine1 = list()
tempo1 = list()
conn = 0



def update_data():
    global ct, sine

    cursor = conn.execute("SELECT oml_sender_id, begin_interval, end_interval, size from iperf_transfer")
    for line in cursor:
        if line[0] == 1:
            temp = line[3]/(1024.0*1024.0)
            temp = temp*8
            sine.append(round(temp,2))
            #sine.append(line[3])
            tempo.append(line[1]*1000)
        else:
            temp1 = line[3]/(1024.0 * 1024.0)
            temp1 = temp1 * 8
            sine1.append(round(temp1,2))
    new_data = dict(x=tempo, y=sine, y1=sine1)
    source.stream(new_data)

    new_data1 = dict(x=tempo, y=sine)
    sourceCong.stream(new_data1)

    new_data2 = dict(x=tempo, y=sine)
    sourceRtt.stream(new_data2)


def start():
    global conn

    conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')
    curdoc().add_timeout_callback(update_data, 100)


# botão start
buttonStart = Button(label="Rodar o Experimento")
buttonStart.on_click(start)


#curdoc().add_root(column(buttonStart, buttonStop, buttonClear, row(fig, fig1), name="ff"))
curdoc().add_root(column(buttonStart, column(fig, figCong, figRtt)))
# curdoc().add_root(row(fig, name="ff"))
# curdoc().add_periodic_callback(update_data, 100)
