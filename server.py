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
FICH = sys.argv[3]

# Errores en los valores: PUERTO y FILE
try:
    PUERTO = int(sys.argv[2])
except ValueError:
    print "Error: Puerto incorrecto"
    raise SystemExit
except IndexError:
    print "Usage: python client.py method receiver@IP:SIPport"
    raise SystemExit

try:
    file = open(FICH, 'r+')
except IOError:
    print "Error: Fichero de audio no encontrado"
    raise SystemExit

metodos_SIP = ("INVITE", "BYE", "ACK")


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
            metodo = line.split()[0]
            direc = line.split()[1]
            sip = line.split()[2]
            protocolo = direc.split(':')[0]
            login_ip = direc.split(':')[1]
            ip_clt = str(self.client_address[0])

            if not metodo in metodos_SIP:
                self.wfile.write('SIP/2.0 405 Method Not Allowed\r\n\r\n')
                print 'Enviando: SIP/2.0 405 Method Not Allowed\r\n\r\n'
            else:
                if protocolo == "sip" and "@" in login_ip and sip == "SIP/2.0":
                    if metodo == 'INVITE':
                        self.wfile.write('SIP/2.0 100 Trying\r\n\r\n')
                        print 'Enviando: ' + 'SIP/2.0 100 Trying\r\n\r\n'
                        self.wfile.write('SIP/2.0 180 Ringing\r\n\r\n')
                        print 'Enviando: ' + 'SIP/2.0 180 Ringing\r\n\r\n'
                        self.wfile.write('SIP/2.0 200 OK\r\n\r\n')
                        print 'Enviando: ' + 'SIP/2.0 200 OK\r\n\r\n'
                    elif metodo == 'ACK':
                        # run: lo que se ha de ejecutar en la shell
                        run = './mp32rtp -i ' + ip_clt + ' -p 23032 < ' + FICH
                        print "Vamos a ejecutar", run
                        os.system(run)
                        print "\r\nEl fichero de audio ha finalizado\r\n\r\n"
                    elif metodo == 'BYE':
                        self.wfile.write('SIP/2.0 200 OK\r\n\r\n')
                        print 'Enviando: ' + 'SIP/2.0 200 OK\r\n\r\n'
                else:
                    self.wfile.write('SIP/2.0 400 Bad Request\r\n\r\n')
                    print 'Enviando: SIP/2.0 400 Bad Request\r\n\r\n'

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PUERTO), EchoHandler)
    print "\nListening...\r\n"
    serv.serve_forever()
