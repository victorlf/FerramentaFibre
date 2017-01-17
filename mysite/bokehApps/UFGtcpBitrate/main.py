#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox
from bokeh.models import Button, RadioButtonGroup, CheckboxButtonGroup, TextInput, Select
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

from  UFGrunExpTbr import run, reWriteExp, insereTabela

source = ColumnDataSource(dict(x=[], y=[], y1=[]))
sourceTCP = ColumnDataSource(dict(x=[], y2=[]))
sourceRTT = ColumnDataSource(dict(x=[], y3=[]))

TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

fig = Figure(tools=TOOLS, plot_width=800, title="Resultado", x_axis_type="datetime")
figTCP = Figure(tools=TOOLS, plot_width=800, title="TCP Congestion", x_axis_type="datetime")
figRTT = Figure(tools=TOOLS, plot_width=800, title="RTT", x_axis_type="datetime")

fig.line(source=source, x='x', y='y', legend="Server Input",line_width=2, color='blue', alpha=0.5)
fig.line(source=source, x='x', y='y1', legend="Client Output",line_width=2, color='red', alpha=0.5)

figTCP.line(source=sourceTCP, x='x', y='y2', legend="TCP Congestion",line_width=2, color='yellow', alpha=0.5)

figRTT.line(source=sourceRTT, x='x', y='y3', legend="RTT",line_width=2, color='green', alpha=0.5)

# Legendas do Gráfico
fig.yaxis.axis_label = "Mbps"
fig.xaxis.axis_label = "Segundos"
fig.legend.location = "bottom_left"
# Legendas do Gráfico
figTCP.yaxis.axis_label = "Packets"
figTCP.xaxis.axis_label = "Segundos"
figTCP.legend.location = "bottom_left"
# Legendas do Gráfico
figRTT.yaxis.axis_label = "ms"
figRTT.xaxis.axis_label = "Segundos"
figRTT.legend.location = "bottom_left"

ct = 0
sine_sum = 0
sine = list()
tempo = list()
sine1 = list()
sine2 = list()
sine3 = list()
tempo1 = list()
tempo2 = list()
tempo3 = list()
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
        transf = "Minstrel Algorithm"
    elif str(new) == "1":
        transf = "PID Algorithm"
    elif str(new) == "2":
        transf = "Fixed Bitrate"


# select
buttonSelect = RadioButtonGroup(labels=["Minstrel Algorithm", "PID Algorithm", "Fixed Bitrate"], active=0)
buttonSelect.on_click(my_radio_handler)
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
    global ct, sine

    global ct, sine, sine1, sine2, sine3, transf, bitRate, nodes, temp_nodes, tempo2, tempo3

    # passando os nós selecionados
    for node in temp_nodes:
        nodes.append(node)

    #reWriteExp("wireless_experiment_4", nodes, transf, size)
    #run(nodes, transf, size)
    insereTabela("victor_tcp_bitrate_experiment_iperf_pid", False, False) #iperf
    insereTabela("victor_tcp_bitrate_experiment_ss_pid", True, False) #cwnd
    insereTabela("victor_tcp_bitrate_experiment_ss_pid", True, True) #rtt

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

    #conn.execute("DELETE  FROM iperf_transfer WHERE oml_sender_id != 100;")
    #conn.commit()
    #conn.close()

    cursor1 = conn.execute("SELECT value from ss_cwnd")

    for i, line in enumerate(cursor1):
        sine2.append(line[0])
        tempo2.append(float(i) * 1000)

    cursor2 = conn.execute("SELECT value from ss_rtt")

    for i, line in enumerate(cursor2):
        sine3.append(line[0])
        tempo3.append(float(i) * 1000)


    fig.yaxis.axis_label = size
    new_data = dict(x=tempo, y=sine, y1=sine1)
    source.stream(new_data)

    new_data1 = dict(x=tempo, y2=sine2)
    sourceTCP.stream(new_data1)

    new_data2 = dict(x=tempo, y3=sine3)
    sourceRTT.stream(new_data2)


def start():
    global conn

    conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')
    curdoc().add_timeout_callback(update_data, 100)


# botão start
buttonStart = Button(label="Rodar o Experimento")
buttonStart.on_click(start)


#curdoc().add_root(column(buttonStart, buttonStop, buttonClear, row(fig, fig1), name="ff"))
curdoc().add_root(row(widgetbox(checkbox_button_group, buttonSelect, select, buttonStart, width=300, height= 50), column(fig, figTCP, figRTT)))
# curdoc().add_root(row(fig, name="ff"))
# curdoc().add_periodic_callback(update_data, 100)
