#! /usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko

from scp import SCPClient
from writeTable import insereTabela

name = "3" #nome que irá diferenciar os arquivos de sq3


def reWriteExp(sq3Name, nodes, transf, size):

    if transf == "TCP":
        udp = "false"
    else:
        udp = "true"

    exp = "wireless_experiment.rb"

    lines = open("experiments/" + exp)
    new_lines = list()
    for line in lines:
        new_lines.append(line)

    for i, line in enumerate(new_lines):
        if "oml-domain" in line:
            new_lines[i] = "    app.setProperty('oml-domain', '" + sq3Name + "')\n"
        elif "Set Iperf UDP" in line:
            new_lines[i] = "defProperty('iperf_isUDP', '" + udp + "', \"Set Iperf UDP\")\n"
        elif "Iperf bandwidth" in line:
            new_lines[i] = "defProperty('iperf_bandwidth', '" + size + "M', 'Iperf bandwidth')\n"
        elif "ID of server node" in line:
            new_lines[i] = "defProperty('server_node','omf.uff.node8',\"ID of server node\")\n"
        elif "ID of client node" in line:
            new_lines[i] = "defProperty('client_node','omf.uff.node1',\"ID of client node\")\n"

    arq = open("experiments/" + exp, "w")
    for line in new_lines:
        arq.writelines(line)

    arq.close()


def run(nodes, transf, size):
    '''Estabelece conexão com a ilha'''

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect('portal.uff.fibre.org.br', port=6622, username='victor@uff', password='familia061293')

    '''Parâmetros a serem passados'''

    exp = "wireless_experiment.rb"
    medicoes = "wireless_experiment_" + name

    '''Primeiro passo, verificar se há nós reservados'''

    stdin, stdout, stderr = ssh.exec_command("omf tell")
    lines = list()
    for row in iter(stdout.readline, b''):
        string = row.rstrip()
        lines.append(str(string))
        print string
    nodes = list()
    #print lines
    for i, line in enumerate(lines):
        if line.startswith("The nodes you have reserved:"):
            x = i + 1
            while not lines[x].startswith("The nodes your command is using:"):
                nodes.append(lines[x])
                x = x + 1

    if len(nodes) != 0:
        print "Os nós reservados foram:\n"
        for node in nodes:
            print str(node) +"\n"
    else:
        print "não há nós reservados"

    '''Segundo, verificar se o experimento requisitado está presente, reescreve o do servidor e o envia para a ilha '''

    if len(stdout.readlines()) == 0:
        print "o experimento não está disponível"
    else:
        print "o experimento " + exp + " está disponível"

    reWriteExp(medicoes, nodes, transf, size)

    with SCPClient(ssh.get_transport()) as scp:
        scp.put("/home/victor/mysite/bokehApps/UFFwireless2/experiments/wireless_experiment.rb", "/home/uff/victor/experiments/wireless_experiment.rb")

    '''Terceiro, rodar o experimento'''

    sucesso = False
    stdin, stdout, stderr = ssh.exec_command("omf exec experiments/" + exp)
    for row in iter(stdout.readline, b''):
         string = row.rstrip()
         msg = str(string)
         if msg.startswith("INFO EXPERIMENT_DONE: Event triggered. Starting the associated tasks"):
             sucesso = True
         print msg

    if sucesso:
        print "Experimento realizado com sucesso!"

    '''Quarto, recurepar as medições do experimento'''

    #Testa se existe um versão antiga do experimento, se sim à apaga
    stdin, stdout, stderr = ssh.exec_command("ls experiments/banco/ | grep " + medicoes)
    if len(stdout.readlines()) != 0:
        ssh.exec_command("rm experiments/banco/" + medicoes)
        print "o arquivo " + medicoes + " antigo, foi apagado!"
    else:
        print "Não há um arquivo " + medicoes + " antigo!"
    #Baixa do servidor oml para minha pasta experiments/banco/
    ssh.exec_command("wget http://localhost:5054/result/dumpDatabase?expID=" + medicoes + " -O experiments/banco/" + medicoes)
    print "Dados Salvos em " + medicoes
    #baixa o arquivo para minha máquina
    with SCPClient(ssh.get_transport()) as scp:
        scp.get("/home/uff/victor/experiments/banco/" + medicoes, "/home/victor/mysite/wired/banco")

    '''Quinto passo, escrever as medições no banco de dados'''

    insereTabela(medicoes)

