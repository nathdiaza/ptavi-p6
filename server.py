#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os

# Servidor UDP simple

# Errores en la línea de comando
if len(sys.argv) != 4:
    print "Usage: python server.py IP port audio_file"
    raise SystemExit
    
# IP del servidor y FICHERO del audio
IP = sys.argv[1]
FICHERO = sys.argv[3]

# Errores en los valores: PUERTO y FILE
try:
    PUERTO = int(sys.argv[2])
except ValueError:
    print "Error: Puerto incorrecto"
    raise SystemExit

try: 
    file = open(FICHERO, 'r+')
except IOError:
    print "Error: Fichero de audio no encontrado"
    raise SystemExit 


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        while 1:
        # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            print "El cliente nos manda " + line
            lista = line.split()
            metodo = lista[0]
        
            if metodo == 'INVITE':
                self.wfile.write('SIP/2.0 100 TRYING\r\n\r\n')
                print 'Enviando: ' + 'SIP/2.0 100 TRYING\r\n\r\n'

                self.wfile.write('SIP/2.0 180 RING\r\n\r\n')
                print 'Enviando: ' + 'SIP/2.0 180 RING\r\n\r\n'

                self.wfile.write('SIP/2.0 200 OK\r\n\r\n')
                print 'Enviando: ' + 'SIP/2.0 200 OK\r\n\r\n'
            elif metodo == 'ACK':
                # aEjecutar es un string con lo que se ha de ejecutar en la shell
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + FICHERO
                print "Vamos a ejecutar", aEjecutar
                os.system(aEjecutar)
                print "El fichero de audio ha finalizado"
            elif metodo == 'BYE':
                self.wfile.write('SIP/2.0 200 OK\r\n\r\n')
                print 'Enviando: ' + 'SIP/2.0 200 OK\r\n\r\n'


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PUERTO), EchoHandler)
    print "\nListening... \r\n"
    serv.serve_forever()
