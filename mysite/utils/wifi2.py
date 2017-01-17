#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from omf.models import Signal

import subprocess
import time
import os


def escreve(essid, signal, channel):
    # print (essid + " " + signal + " CH: " + channel)
    #s = Signal(name=essid, signal=signal, channel=channel)
    #s.save()
    print (signal)


class Dump:

    def __init__(self):

        self.password = "061293\n"
        self.p = self.p = subprocess.Popen(["sudo", "-S", "whoami"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.p.communicate(self.password)

    def pr(self):
        print

    def stop(self):
        pid = str(self.p.pid)
        print(pid)
        subprocess.call(["sudo", "kill", pid])

    def monitor(self):

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

                if essid.startswith("B"):
                    escreve(essid, signal, channel)
                    # arq = open('sinal.txt', 'w')
                    # arq.write(signal)
                    # arq.close
                    # print signal
                    pid = str(self.p.pid)
                    subprocess.call(["sudo", "kill", pid])

            #time.sleep(3)


def main():

    d = Dump()
    d.monitor()
    time.sleep(10)
    d.stop()
#main()

#bokeh serve bokehApps/wireless bokehApps/wired --allow-websocket-origin=localhost:8000
