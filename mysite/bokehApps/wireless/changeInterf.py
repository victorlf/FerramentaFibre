#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import system

import subprocess

password = "061293\n"
p = subprocess.Popen(["sudo", "-S", "whoami"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p.communicate(password)

system("sudo iw phy phy0 interface add mon0 type monitor")
system("sudo ifconfig wlan0 down")
system("sudo ifconfig mon0 up")

#change freq
#p = subprocess.Popen(["sudo", "iw", "dev", "mon0", "set", "freq", "2437"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
