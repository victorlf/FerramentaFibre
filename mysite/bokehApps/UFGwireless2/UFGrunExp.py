#! /usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import sqlite3

from scp import SCPClient


name = "3" #nome que irá diferenciar os arquivos de sq3


def reWriteExp(sq3Name, nodes, transf, size):

    if transf == "TCP":
        udp = "false"
    else:
        udp = "true"

    for i, node in enumerate(nodes):
        node = node.strip(" ")
        if node == "0":
            nodes[i] = "node1"
        elif node == "1":
            nodes[i] = "node7"
        elif node == "2":
            nodes[i] = "node8"
        elif node == "3":
            nodes[i] = "node9"

    exp = "wireless_experiment.rb"

    lines = open("/home/victor/mysite/bokehApps/UFGwireless2/experiments/" + exp)
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
            new_lines[i] = "defProperty('server_node','omf.ufg." + nodes[0] + "',\"ID of server node\")\n"
        elif "ID of client node" in line:
            new_lines[i] = "defProperty('client_node','omf.ufg." + nodes[1] + "',\"ID of client node\")\n"

    arq = open("/home/victor/mysite/bokehApps/UFGwireless2/experiments/" + exp, "w")
    for line in new_lines:
        arq.writelines(line)

    arq.close()


def insereTabela(arquivo):
    params = []
    # medicoes = "wireless_experiment_iperf_victor"

    # lines = open("/home/victor/myDatabase.sq3")
    lines = open("/home/victor/mysite/bokehApps/UFGwireless2/banco/" + arquivo)
    tup = ()
    for line in lines:
        # Assim pula linhas indesejadas
        if line.startswith("INSERT INTO \"iperf_transfer\""):
            cells = line.split()
            # print cells
            for i, cell in enumerate(cells):
                if cell.startswith("VALUES"):
                    cellValue = cell.replace("VALUES", "")
                    cellValue = cellValue.replace(";", "")
                    cellValue = cellValue.replace("(", "")
                    cellValue = cellValue.replace(")", "")
                    temp = cellValue.split(",")
                    for val in temp:
                        temp2 = (val,)
                        tup = tup + temp2
                    params.append(tup)
                    tup = ()
                    cells[i] = "VALUES(?,?,?,?,?,?,?,?,?,?,?);"
                    # print cells

    conn = sqlite3.connect('/home/victor/mysite/db.sqlite3')
    sql = "INSERT INTO IPERF_TRANSFER  (OML_TUPLE_ID, OML_SENDER_ID, OML_SEQ, OML_TS_CLIENT, OML_TS_SERVER, PID, CONNECTION_ID , BEGIN_INTERVAL, END_INTERVAL, SIZE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? ,?)"
    i = 1
    for param in params:
        conn.execute(sql, param)
        print i
        i += 1
    conn.commit()
    conn.close()

def run(nodes, transf, size):
    '''Estabelece conexão com a ilha'''

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect('portal.ufg.fibre.org.br', port=6622, username='victor@ufg', password='familia061293')

    '''Parâmetros a serem passados'''

    exp = "wireless_experiment.rb"
    medicoes = "wireless_experiment_" + name#data+hora

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
        scp.put("/home/victor/mysite/bokehApps/UFGwireless2/experiments/wireless_experiment.rb", "/home/ufg/victor/experiments/wireless_experiment.rb")

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
        scp.get("/home/ufg/victor/experiments/banco/" + medicoes, "/home/victor/mysite/wired/banco")

    '''Quinto passo, escrever as medições no banco de dados'''

    return insereTabela(medicoes)

