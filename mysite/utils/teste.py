# -*- coding: latin1 -*-
"""
Exemplo de uso de threads
"""
import os
import time
import threading


class Monitor(threading.Thread):
    """
    Classe de monitoramento usando threads
    """
    def __init__(self, ip):
        """
        Construtor da thread
        """
        # Atributos para a thread
        self.ip = ip
        self.status = None
        # Inicializador da classe Thread
        threading.Thread.__init__(self)

    def run(self):
        """
        Código que será executado pela thread
        """
        # Execute o ping
        ping = os.popen('ping -n 1 %s' % self.ip).read()
        if 'unreachable' in ping:
            self.status = False
        else:
            self.status = True

if __name__ == '__main__':

    # Crie uma lista com um objeto de thread para cada IP
    monitores = []
    for i in range(1, 11):
        ip = '10.10.10.%d' % i
        monitores.append(Monitor(ip))
    # Execute as Threads
    for monitor in monitores:
        monitor.start()
    # A thread principal continua enquanto
    # as outras threads executam o ping
    # para os endereços da lista
    # Verifique a cada segundo
    # se as threads acabaram
    ping = True
    while ping:
        ping = False
        for monitor in monitores:
            if monitor.status == None:
                ping = True
                break
        time.sleep(1)
    # Imprima os resultados no final
    for monitor in monitores:

        if monitor.status:
            print '%s no ar' % monitor.ip
        else:
            print '%s fora do ar' % monitor.ip

