#! /usr/bin/env python
# -*- coding: utf-8 -*-

from oml4py import OMLBase

import subprocess


def printTable(time, ttl, mac):
    table = OMLBase("ping", "mysite", "noMovel", "tcp:10.134.11.106:3003")
    table.addmp("notebook", "time:double ttl:double mac:string")
    table.start()
    table.inject("notebook", (time, ttl, mac))
    table.close()

def findMac():
    p1 = subprocess.Popen(('iwconfig'), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(('grep', 'Access Point'), stdin=p1.stdout, stdout=subprocess.PIPE)
    for row in iter(p2.stdout.readline, b''):
        string = row.rstrip()
        cells = string.split()
        return cells[5]


p = subprocess.Popen(('ping', '-I', 'wlan0', '8.8.8.8'), stdout=subprocess.PIPE)
for row in iter(p.stdout.readline, b''):
    string = row.rstrip()
    cells = string.split()
    if cells[5] == "Unreachable":
        time = "0"
        ttl = "0"
    else:
        time = cells[6]
        time = time.replace("time=", "")
        ttl = cells[5].replace("ttl=", "")
        mac = findMac()
        if time != "data.":
            print time, ttl, findMac()
    printTable(time, ttl, mac)

