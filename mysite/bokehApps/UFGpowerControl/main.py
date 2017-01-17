#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox
from bokeh.models import Button, RadioButtonGroup, CheckboxButtonGroup, TextInput, Select
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

from  UFGrunExpPC import run, reWriteExp, insereTabela

source = ColumnDataSource(dict(x=[], y=[], x1=[], y1=[]))
sourceRssi = ColumnDataSource(dict(x2=[], y2=[]))

TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

fig = Figure(tools=TOOLS, plot_width=800, title="Resultado", x_axis_type="datetime")
figRssi = Figure(tools=TOOLS, plot_width=800, title="RSSI", x_axis_type="datetime")

fig.line(source=source, x='x', y='y', legend="Server Input",line_width=2, color='blue', alpha=0.5)
fig.line(source=source, x='x1', y='y1', legend="Client Output",line_width=2, color='red', alpha=0.5)

figRssi.line(source=sourceRssi, x='x2', y='y2', legend="RSSI",line_width=2, color='yellow', alpha=0.5)

# Legendas do Gráfico
fig.yaxis.axis_label = "Mbps"
fig.xaxis.axis_label = "Segundos"
fig.legend.location = "bottom_left"
# Legendas do Gráfico
figRssi.yaxis.axis_label = "dbm"
figRssi.xaxis.axis_label = "Segundos"
figRssi.legend.location = "bottom_left"

ct = 0
sine_sum = 0
sine = list()
tempo = list()
tempo1 = list()
tempo2 = list()
sine1 = list()
sine2 = list()
conn = 0

#select and input vars
power = "15" #Caso o clique não aconteça
nodes = list()
temp_nodes = ""
univ = ""
bitRate = "54"

#select event
def my_select_handler(attr, old, new):
    global power
    power = str(new)


# select
buttonSelect = Select(title="Tx Power(dbm):", value="15",options=["0", "1", "2", "5", "10", "15"])
buttonSelect.on_change('value', my_select_handler)
#input event
def my_text_input_handler(attr, old, new):
    global bitRate
    bitRate = str(new)

#input para UDP
#text_input = TextInput(value="15", title="Fixed bitrate values:")
select = Select(title="Fixed bitrate values (Mbits):", value="54", options=["6", "9", "12", "18", "24", "36", "48", "54"])
select.on_change('value', my_text_input_handler)

#checkbox event
def my_checkbox_handler(new):
    global temp_nodes
    temp_nodes = str(new)
    temp_nodes = temp_nodes.replace("[", "")
    temp_nodes = temp_nodes.replace("]", "")
    temp_nodes = temp_nodes.split(",")

#checkbox nodes
checkbox_button_group = CheckboxButtonGroup(labels=["Node 1", "Node 7", "Node 8", "Node 9"])
checkbox_button_group.on_click(my_checkbox_handler)

def update_data():

    global ct, sine, sine1, sine2, power, bitRate, nodes, temp_nodes

    # passando os nós selecionados
    for node in temp_nodes:
        nodes.append(node)
    print nodes, bitRate, power
    #reWriteExp("wireless_experiment_4", nodes, bitRate, power)
    #run(nodes, bitRate, power)
    #insereTabela("victor_power_control_experiment_iperf", False)
    #insereTabela("victor_power_control_experiment_iwdata", True)


    cursor = conn.execute("SELECT oml_sender_id, begin_interval, end_interval, size from iperf_transfer")

    for line in cursor:
        if line[0] == 1:
            temp = line[3] / (1024.0 * 1024.0)
            temp = temp * 8
            sine.append(round(temp, 2))
            tempo.append(line[1] * 1000)
        else:
            temp1 = line[3] / (1024.0 * 1024.0)
            temp1 = temp1 * 8
            sine1.append(round(temp1, 2))
            tempo1.append(line[1] * 1000)

    #conn.execute("DELETE  FROM iperf_transfer WHERE oml_sender_id != 100;")
    #conn.commit()
    #conn.close()
    #fig.yaxis.axis_label = size

    cursor = conn.execute("SELECT value from iwconfig_rssi")

    for i,line in enumerate(cursor):
        sine2.append(line[0])
        tempo2.append(float(i)*1000)

    # conn.execute("DELETE  FROM iwconfig_rssi WHERE oml_sender_id != 100;")
    # conn.commit()
    # conn.close()

    new_data = dict(x=tempo, y=sine, x1=tempo1, y1=sine1)
    source.stream(new_data)

    new_data1 = dict(x2=tempo2, y2=sine2)
    sourceRssi.stream(new_data1)


def start():
    global conn

    conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')
    curdoc().add_timeout_callback(update_data, 100)


# botão start
buttonStart = Button(label="Rodar o Experimento")
buttonStart.on_click(start)


#curdoc().add_root(column(buttonStart, buttonStop, buttonClear, row(fig, fig1), name="ff"))
curdoc().add_root(row(widgetbox(checkbox_button_group, buttonSelect, select, buttonStart, width=300), column(fig, figRssi)))
# curdoc().add_root(row(fig, name="ff"))
# curdoc().add_periodic_callback(update_data, 100)
