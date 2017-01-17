#! /usr/bin/env python
# -*- coding: utf-8 -*-

#*************************** MÓDULO DO TREM ************************************
#esse script rodará dentro do OMF, logo não precisamos de entrar em nenhuma rede
#caso necessário, inserir o comando para tal no código que chamará esse módulo 

import os
#import time
import urllib2

#Comandos para o Carro

def fwd():
    """Faz o trem andar para frente."""
    urllib2.urlopen('http://10.134.11.23/cgi-bin/fwd.cgi')

def halt():
    """Faz o trem parar."""
    #os.system('wget 10.134.11.23/cgi-bin/halt.cgi')
    urllib2.urlopen('http://10.134.11.23/cgi-bin/halt.cgi')

def bwd():
    """Faz o trem andar para trás."""
    #os.system('wget 10.134.11.23/cgi-bin/bwd.cgi')
    urllib2.urlopen('http://10.134.11.23/cgi-bin/bwd.cgi')

def log():
    """	Mostra os logs de uso.	"""
    os.system('wget 10.134.11.23/cgi-bin/log.cgi')
        
def status():
    """
    retorna a posição do Carro
    """
    if os.path.isfile('status.cgi'):
        os.remove('status.cgi')
    #os.system('wget 10.134.11.23/cgi-bin/status.cgi')
    list = urllib2.urlopen('http://10.134.11.23/cgi-bin/status.cgi').read().split("\n")
    #time.sleep(0.1) #é o menor tempo possível, abaixo disso não temos resposta
    #temp = open('status.cgi')
    #list =  temp.readlines()
    a = int(list[8])
    print type(a)   #Feito para depurar o código
    print list  #Feito para depurar o código
    print a #Feito para depurar o código
    return a
    #temp.close()

def fwd_set_dist(dist):
    """
	Faz o Carro andar a distância passada
	"""
    #não conseguindo, fazer pelo tempo
    a = status()
    if a == dist:
        return 'O Carro já está nesse ponto'
        #break
    elif dist > a:
        fwd()
        while dist > a :
            a = status()
            """if a >= dist:
                halt()
                return 'O Carro chegou ao seu ponto'
                break"""
        halt()
        return 'O Carro chegou ao seu ponto' + str(a)
        #break
    elif dist < a:
        bwd()
        while dist < a :
            a = status()
            """if a <= dist:
                halt()
                return 'O Carro chegou ao seu ponto'
                break"""
        halt()
        return 'O Carro chegou ao seu ponto' + str(a)
        #break

               

#Comandos para o Notebook

#def bateria():
    """
	verifica o estado da bateria
	Procurar no final do comando a linha: "on-battery: no", isso nos diz que o Notebook está carregando
	"""
    #scriptine.shell.sh('ssh omf@10.134.11.24 upower -d')