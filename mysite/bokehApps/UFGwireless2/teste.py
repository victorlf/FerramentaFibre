#! /usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
from scp import SCPClient

'''Estabelece conexão com a ilha'''

exp = "wireless_experiment.rb"
name = "dois"
sq3Name = "wireless_experiment_" + name

# ssh = paramiko.SSHClient()
# ssh.load_system_host_keys()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# ssh.connect('portal.ufg.fibre.org.br', port=6622, username='victor@ufg', password='familia061293')
#
# with SCPClient(ssh.get_transport()) as scp:
#     scp.get("/home/ufg/victor/experiments/victor_wireless_experiment.rb", "/home/victor/mysite/bokehApps/UFGwireless2/experiments/wireless_experiment.rb")

lines = open("experiments/" + exp)
new_lines = list()
for line in lines:
    new_lines.append(line)

for i,line in enumerate(new_lines):
    if "oml-domain" in line:
        # new_lines[i] = "    app.setProperty('oml-domain', '"+ sq3Name +"')\n"
        print line

# arq = open("experiments/" + exp, "w")
# for line in new_lines:
#    arq.writelines(line)

#arq.close()
#
# ssh = paramiko.SSHClient()
# ssh.load_system_host_keys()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# ssh.connect('portal.ufg.fibre.org.br', port=6622, username='victor@ufg', password='familia061293')
#
# with SCPClient(ssh.get_transport()) as scp:
#     scp.put("/home/victor/mysite/bokehApps/UFGwireless2/experiments/wireless_experiment.rb", "/home/ufg/victor/experiments/wireless_experiment.rb")
