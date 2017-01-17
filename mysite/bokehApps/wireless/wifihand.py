#! /usr/bin/env python
# -*- coding: utf-8 -*-

from oml4py import OMLBase

import subprocess
import time


def printTable(time):
    table = OMLBase("ping", "mysite", "noMovel", "tcp:10.134.11.106:3003")
    table.addmp("notebook", "time:int32")
    table.start()
    table.inject("notebook", time)
    table.close()


def findMac():
    p1 = subprocess.Popen(('iwconfig'), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(('grep', 'Access Point'), stdin=p1.stdout, stdout=subprocess.PIPE)
    for row in iter(p2.stdout.readline, b''):
        string = row.rstrip()
        cells = string.split()
        return cells[5]

p = subprocess.Popen(('ping', '-I', 'wlan0', '8.8.8.8'), stdout=subprocess.PIPE)
#time.sleep(10)
for row in iter(p.stdout.readline, b''):
    string = row.rstrip()
    cells = string.split()
    #print cells
    if cells[5] == "Unreachable":
        time = "0"
        print time
    else:
        time = cells[6]
        time = time.replace("time=", "")
        if time != "data.":
            #printTable(time)
            print time, findMac()

