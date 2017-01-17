#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox
from bokeh.models import Button, Select, RadioButtonGroup, CheckboxButtonGroup, TextInput
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

from runExp import run

import sqlite3



source = ColumnDataSource(dict(x=[], y=[], y1=[]))

TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
fig = Figure(tools=TOOLS, plot_width=800, title="Resultado", x_axis_type="datetime")


#fig.line(source=source, x='x', y='y', line_dash=[4, 4], alpha=85, color='blue')
fig.line(source=source, x='x', y='y', legend="Server Input",line_width=2, color='blue', alpha=0.5)
#fig.circle(source=source, x='x', y='y', legend="Server Input", fill_color="white",size=8)
fig.line(source=source, x='x', y='y1', legend="Client Output",line_width=2, color='red', alpha=0.5)
#fig.square(source=source, x='x', y='y1', legend="Client Output", fill_color="white", size=8)

# fig.line(source=source, x='x', y='y', line_dash="4 4", line_width=1, color='gray')
# cr = fig.circle(source=source, x='x', y='y', size=20,
#                 fill_color="grey", hover_fill_color="firebrick",
#                 fill_alpha=0.05, hover_alpha=0.3,
#                 line_color=None, hover_line_color="white")
# fig.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='hline'))


# Legendas do Gráfico
fig.yaxis.axis_label = "Mbps"
fig.xaxis.axis_label = "Segundos"
fig.legend.location = "bottom_left"

ct = 0
sine_sum = 0
sine = list()
tempo = list()
sine1 = list()
tempo1 = list()
conn = 0

#select and input vars
transf = "TCP" #Caso o clique não aconteça
size = "15"
nodes = list()
temp_nodes = ""
univ = ""

#select event
def my_radio_handler(new):
    global transf
    if str(new) == "0":
        transf = "TCP"
    else:
        transf = "UDP"


# select
buttonSelect = RadioButtonGroup(labels=["TCP", "UDP"], active=0)
buttonSelect.on_click(my_radio_handler)

#input event
def my_text_input_handler(attr, old, new):
    global size
    temp = str(new)
    #verifica se foi digitado apenas numeros
    if temp.isdigit():
        size = temp

#input para UDP
text_input = TextInput(value="15", title="Iperf bandwidth size (Mbits) [Apenas UDP]:")
text_input.on_change("value", my_text_input_handler)

#checkbox event
def my_checkbox_handler(new):
    global temp_nodes
    temp_nodes = str(new)
    temp_nodes = temp_nodes.replace("[", "")
    temp_nodes = temp_nodes.replace("]", "")
    temp_nodes = temp_nodes.split(",")

#checkbox nodes
checkbox_button_group = CheckboxButtonGroup(labels=["Node 1", "Node 2", "Node 3", "Node 4"])
checkbox_button_group.on_click(my_checkbox_handler)


def update_data():
    global ct, sine, transf, size, nodes, temp_nodes

    cursor = conn.execute("SELECT oml_sender_id, begin_interval, end_interval, size from iperf_transfer")
    for line in cursor:
        if line[0] == 1:
            temp = line[3]/(1024.0*1024.0)
            temp = temp*8
            sine.append(round(temp,2))
            tempo.append(line[1]*1000)
        else:
            temp1 = line[3]/(1024.0 * 1024.0)
            temp1 = temp1 * 8
            sine1.append(round(temp1,2))
    new_data = dict(x=tempo, y=sine, y1=sine1)
    source.stream(new_data)

    for node in temp_nodes:
        nodes.append(node)
    fig.yaxis.axis_label = "UFF"

    #run(nodes, transf, size)


def start():
    global conn

    conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')
    curdoc().add_timeout_callback(update_data, 100)



# botão start
buttonStart = Button(label="Rodar o Experimento")
buttonStart.on_click(start)

#curdoc().add_root(column(buttonStart, buttonStop, buttonClear, row(fig, fig1), name="ff"))
curdoc().add_root(row(widgetbox( checkbox_button_group, buttonSelect, text_input, buttonStart, width=300), fig))
# curdoc().add_root(row(fig, name="ff"))
# curdoc().add_periodic_callback(update_data, 100)
