#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import subprocess

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Button
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

import wifi
import sqlite3

source = ColumnDataSource(dict(x=[], y=[]))

fig = Figure()
fig.line(source=source, x='x', y='y', line_width=2, alpha=85, color='red')

ct = 0
ct1 = 0
sine = 0


def update_data():
    global ct, ct1, sine
    ct += 1
    ct1 += 1
    conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')
    cursor = conn.execute(
        "SELECT id, name, signal,channel FROM omf_signal WHERE id = (SELECT MAX(id) FROM omf_signal) ")
    for line in cursor:
        sine = line[2]
    conn.close()
    new_data = dict(x=[ct], y=[sine])
    source.stream(new_data, 100)


def start():

    curdoc().add_periodic_callback(update_data, 2000)


def stop():
    curdoc().remove_periodic_callback(update_data)

# botão start
buttonStart = Button(label="Start")
buttonStart.on_click(start)

# botão stop
buttonStop = Button(label="Stop")
buttonStop.on_click(stop)

curdoc().add_root(column(buttonStart, buttonStop, fig))
#curdoc().add_periodic_callback(update_data, 100)

