#! /usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process

import paramiko

class Ping():

    def run(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect( '10.134.11.24', username='omf', password='omf' )
        stdin, stdout, stderr  = ssh.exec_command("python /home/omf/mysite/wifihand.py")

        for row in iter(stderr.readline, b''):
            string = row.rstrip()
            print string