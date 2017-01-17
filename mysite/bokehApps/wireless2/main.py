#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import subprocess

from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox
from bokeh.models import Button
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

import wifi
import sqlite3

#from pingSSH import runPing
from pingSSH import Ping

import threading
from multiprocessing import Process


source = ColumnDataSource(dict(x=[], y=[], text=[]))

TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

#source1 = ColumnDataSource(dict(x=[], y=[]))

#fig = Figure(name="plot", title="Signal level (dBm)")
fig = Figure(tools=TOOLS, plot_width=600, plot_height=500, title="Resultado")
fig.line(source=source, x='x', y='y', legend="Response Time", line_width=2, alpha=85, color='red')
fig.text(source=source, text='text', text_font_size="15pt", text_baseline="bottom", text_align="left")
#fig.line(source=source, x='x', y='avg', line_width=2, alpha=85, color='blue')

#fig1 = Figure(name="plot")
#fig1.line(source=source1, x='x', y='y', line_width=2, alpha=85, color='red')

fig.yaxis.axis_label = "ms"
fig.xaxis.axis_label = "Distância"
fig.legend.location = "bottom_right"

ct = 0
sine_sum = 0
sine = 0
conn = 0



def update_data():
    global ct, sine
    # sine_sum += sine
    #sine = wifi2.main()
    sine = 0
    ct += 1
    #cursor = conn.execute("SELECT id, name, signal, channel from omf_signal WHERE id = (SELECT MAX(id) from omf_signal) ")
    cursor = conn.execute("SELECT oml_tuple_id, time, mac from ping_notebook WHERE oml_tuple_id = (SELECT MAX(oml_tuple_id) from ping_notebook) ")
    for line in cursor:
        sine = line[1]
        mac = line[2]
   # new_data = dict(x=[ct], y=[sine], avg=[sine_sum/ct])
    new_data = dict(x=[ct], y=[sine], text=[mac])
    source.stream(new_data, 100)


#def update_data():
#    global ct, sine_sum
#    ct += 1source=source, x='x', y='y',
#    sines = wifi.main()
#    new_data = dict(x=[ct], y=[sines[0]])
#    source.stream(new_data, 100)
#    new_data1 = dict(x=[ct], y=[sines[1]])
#    source1.stream(new_data1, 100)


def start():
    global conn
    #d = Dump()
    #p1 = Process(target = d.monitor)
    #p1 = Process(target=runPing())
    #d = Ping()
    #p1 = Process(target= d.run)
    #p1.start()

    #conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')
    conn = sqlite3.connect('/var/lib/oml2/mysite.sq3')
    curdoc().add_periodic_callback(update_data, 100)

# def start():
#     global conn
#
#     class Tt(threading.Thread):
#
#         def __init__(self):
#             # Inicializador da classe Thread
#             threading.Thread.__init__(self)
#
#         def monit(self):
#             d = Dump()
#             d.monitor()
#
#         def up(self):
#             return sqlite3.connect('/home/victor/mysite/db.sqlite3')
#
#     t = Tt()
#     t.monit()
#     conn = t.up()
#     curdoc().add_periodic_callback(update_data, 1000)



def stop():
    conn.close()
    curdoc().remove_periodic_callback(update_data)


def clear():
    # ColumnDataSource.remove('y')
    # plotToRemove = curdoc().get_model_by_name('plot')
    # ColumnDataSource().remove('y')

    print "oioioioiooi"


# botão start
buttonStart = Button(label="Rodar o Experimento")
buttonStart.on_click(start)

# botão stop
buttonStop = Button(label="Stop")
buttonStop.on_click(stop)

# botão clear
buttonClear = Button(label="Limpar")
buttonClear.on_click(clear)

#curdoc().add_root(column(buttonStart, buttonStop, buttonClear, row(fig, fig1), name="ff"))
curdoc().add_root(row(widgetbox(buttonStart, buttonStop), fig, name="ff"))
#curdoc().add_root(row(fig, fig1, name="ff"))
#curdoc().add_periodic_callback(update_data, 100)
