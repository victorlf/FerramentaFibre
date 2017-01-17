#! /usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import sqlite3

from scp import SCPClient


name = "1" #nome que irá diferenciar os arquivos de sq3


def reWriteExp(sq3Name, nodes, bitRate, power):

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

    exp = "power_control_experiment.rb"

    lines = open("/home/victor/mysite/bokehApps/UFGpowerControl/experiments/" + exp)
    new_lines = list()
    for line in lines:
        new_lines.append(line)

    for i, line in enumerate(new_lines):
        if "oml-domain" in line:
            if "tutorials:iwdata" in new_lines[i-4]:
                new_lines[i] = "    app.setProperty('oml-domain', '" + sq3Name + "iwdata')\n"  # muda o nome do arquivo do iperf
            else:
                new_lines[i] = "    app.setProperty('oml-domain', '" + sq3Name + "')\n" # muda o nome do arquivo do iperf
        elif "Fixed bitrate value." in line:
            new_lines[i] = "defProperty('bitrate', '"+ bitRate + "', 'Fixed bitrate value.')\n"
        elif "Server Tx Power" in line:
            new_lines[i] = "defProperty('server_tx_power', '" + power + "', 'Server Tx Power')\n"
        elif "Client Tx Power" in line:
            new_lines[i] = "defProperty('client_tx_power', '" + power + "', 'Client Tx Power')\n"
        elif "ID of server node" in line:
            new_lines[i] = "defProperty('server_node','omf.ufg." + nodes[1] + "',\"ID of server node\")\n"
        elif "ID of client node" in line:
            new_lines[i] = "defProperty('client_node','omf.ufg." + nodes[0] + "',\"ID of client node\")\n"

    arq = open("/home/victor/mysite/bokehApps/UFGpowerControl/experiments/" + exp, "w")
    for line in new_lines:
        arq.writelines(line)

    arq.close()
    print "rodei"

def insereTabela(arquivo, rssi):
    params = []

    if rssi:
        table = "INSERT INTO \"iwconfig_rssi\""
        insere = "INSERT INTO IWCONFIG_RSSI  (OML_TUPLE_ID, OML_SENDER_ID, OML_SEQ, OML_TS_CLIENT, OML_TS_SERVER, TIMESTAMP, VALUE) VALUES (?, ?, ?, ?, ?, ?, ?)"
    else:
        table = "INSERT INTO \"iperf_transfer\""
        insere = "INSERT INTO IPERF_TRANSFER  (OML_TUPLE_ID, OML_SENDER_ID, OML_SEQ, OML_TS_CLIENT, OML_TS_SERVER, PID, CONNECTION_ID , BEGIN_INTERVAL, END_INTERVAL, SIZE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? ,?)"


    lines = open("/home/victor/mysite/bokehApps/UFGpowerControl/banco/" + arquivo)
    tup = ()
    for line in lines:
        # Assim pula linhas indesejadas
        if line.startswith(table):
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
    sql = insere
    i = 1
    for param in params:
        conn.execute(sql, param)
        print i
        i += 1
    conn.commit()
    conn.close()

def run(nodes_selected, bitRate, power):
    '''Estabelece conexão com a ilha'''

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect('portal.ufg.fibre.org.br', port=6622, username='victor@ufg', password='familia061293')

    '''Parâmetros a serem passados'''

    exp = "power_control_experiment.rb"
    medicoes = "wireless_experiment_" + name#data+hora
    medicoesRssi = medicoes + "iwdata"

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

    reWriteExp(medicoes, nodes_selected, bitRate, power)

    with SCPClient(ssh.get_transport()) as scp:
        scp.put("/home/victor/mysite/bokehApps/UFGpowerControl/experiments/" + exp, "/home/ufg/victor/experiments/" + exp)

    '''Terceiro, rodar o experimento'''

    sucesso = False
    stdin, stdout, stderr = ssh.exec_command("omf exec experiments/" + exp)
    for row in iter(stdout.readline, b''):
         string = row.rstrip()
         #msg = str(string)
         print string
         #if msg.startswith("INFO EXPERIMENT_DONE: Event triggered. Starting the associated tasks"):
         #    sucesso = True
         #print msg

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

    stdin, stdout, stderr = ssh.exec_command("ls experiments/banco/ | grep " + medicoesRssi)
    if len(stdout.readlines()) != 0:
        ssh.exec_command("rm experiments/banco/" + medicoesRssi)
        print "o arquivo " + medicoesRssi + " antigo, foi apagado!"
    else:
        print "Não há um arquivo " + medicoesRssi + " antigo!"
    #Baixa do servidor oml para minha pasta experiments/banco/
    ssh.exec_command("wget http://localhost:5054/result/dumpDatabase?expID=" + medicoes + " -O experiments/banco/" + medicoes)
    print "Dados Salvos em " + medicoes
    ssh.exec_command("wget http://localhost:5054/result/dumpDatabase?expID=" + medicoesRssi + " -O experiments/banco/" + medicoesRssi)
    print "Dados Salvos em " + medicoesRssi
    #baixa o arquivo para minha máquina
    with SCPClient(ssh.get_transport()) as scp:
        scp.get("/home/ufg/victor/experiments/banco/" + medicoes, "/home/victor/mysite/bokehApps/UFGpowerControl/banco")
    with SCPClient(ssh.get_transport()) as scp:
        scp.get("/home/ufg/victor/experiments/banco/" + medicoesRssi, "/home/victor/mysite/bokehApps/UFGpowerControl/banco")

    '''Quinto passo, escrever as medições no banco de dados'''

    insereTabela(medicoes, False)
    insereTabela(medicoesRssi, True)

