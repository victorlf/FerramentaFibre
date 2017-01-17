#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from omf.models import Signal
from os import system

import subprocess
import time
import os
import sqlite3
from oml4py import OMLBase


def escreve(essid, signal, channel):
    ## print (essid + " " + signal + " CH: " + channel)
    ##s = Signal(name=essid, signal=signal, channel=channel)
    ##s.save()
    #conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')
    ##conn.execute("INSERT INTO omf_signal (id, name, signal, channel) VALUES (2,"+ essid + "," + signal + "," + channel+");")
    #params = (essid, "none", "none", signal, channel, "none", "none")
    #sql = "INSERT INTO OMF_SIGNAl  ( NAME, ADRESS, QUALITY, SIGNAL, CHANNEL, ENCRYPTION, TIME) VALUES (?, ?, ?, ?, ?, ?, ?)"
    #onn.execute(sql, params)
    ##conn.execute("INSERT INTO OMF_SIGNAl  ( NAME, ADRESS, QUALITY, SIGNAL, CHANNEL, ENCRYPTION, TIME) VALUES (1,2,3,4,5,6,7)")
    #conn.commit()
    ##print "salvo"
    #print (signal)

    table = OMLBase("tcpDump", "mysite", "noMovel", "tcp:10.134.11.106:3003")
    table.addmp("notebook", "essid:string signal:int32 channel:int32")
    table.start()
    table.inject("notebook", (essid, signal, channel))
    table.close()



class Dump:

    def __init__(self):

        self.password = "omf\n"
        self.p = self.p = subprocess.Popen(["sudo", "-S", "whoami"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.p.communicate(self.password)
        system("sudo iw phy phy0 interface add mon0 type monitor")
        system("sudo ifconfig wlan0 down")
        system("sudo ifconfig mon0 up")

    def pr(self):
        print

    def stop(self):
        pid = str(self.p.pid)
        print(pid)
        subprocess.call(["sudo", "kill", pid])

    def monitor(self):

        # Antes de fazer a captura devemos deletar todos os registros antigos da tabela
        # conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')
        # sql = "SELECT id, name from omf_signal WHERE id = (SELECT MAX(id) from omf_signal) "
        # cursor = conn.execute(sql)
        # for line in cursor:
        #     name = line[1]
        # params = (name,)
        # sql = "DELETE from OMF_signal where Name = ?"
        # conn.execute(sql, params)
        # conn.commit()
        # conn.close()

        self.p = subprocess.Popen(('sudo', 'tcpdump', '-l'), stdout=subprocess.PIPE)
        for row in iter(self.p.stdout.readline, b''):
            string = row.rstrip()
            if "Beacon" in string:
                cells = []
                essid = ""
                signal = ""
                channel = ""

                cells = string.split()
                for i, cell in enumerate(cells):
                    if cell == "Beacon":
                        essid = cells[i + 1].replace("(","")
                        essid = essid.replace(")","")
                    elif cell == "signal":
                        signal = cells[i - 1].replace("dB", "")
                    elif cell.startswith("CH"):
                        channel = cells[i + 1].replace(",", "")

                if essid.startswith("BNDVIS"):
                    escreve(essid, signal, channel)
                    # arq = open('sinal.txt', 'w')
                    # arq.write(signal)
                    # arq.close
                    # print signal
                    #pid = str(self.p.pid)
                    #subprocess.call(["sudo", "kill", pid])

            #time.sleep(3)


def main():

    d = Dump()
    d.monitor()
    time.sleep(10)
    d.stop()
#main()

#bokeh serve bokehApps/wireless bokehApps/wired --allow-websocket-origin=localhost:8000
