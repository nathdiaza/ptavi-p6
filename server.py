#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en SIP simple
"""

import SocketServer
import sys
import os

# Errores en la línea de comando
if len(sys.argv) != 4:
    print "Usage: python server.py IP port audio_file"
    raise SystemExit

# IP del servidor y FICHERO del audio
IP = sys.argv[1]
fich_audio = sys.argv[3]

# Errores en los valores: PUERTO y FILE
try:
    PORT = int(sys.argv[2])
except ValueError:
    print "Error: Puerto incorrecto"
    raise SystemExit
except IndexError:
    print "Usage: python client.py method receiver@IP:SIPport"
    raise SystemExit

try:
    file = open(fich_audio, 'r+')
except IOError:
    print "Error: Fichero de audio no encontrado"
    raise SystemExit


class SIPHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class(INVITE,ACK y BYE)
    """
    def handle(self):

        while 1:
            line = self.rfile.read()
            if not line:
                break
            print line
            print "El cliente nos manda " + line
            line = line.split(" ")
            method = line[0]
            if "SIP/2.0\r\n\r\n" not in line:
                self.wfile.write("SIP/2.0 400 Bad Request\r\n\r\n")
                print 'Enviando: SIP/2.0 400 Bad Request\r\n\r\n'
            elif method == "INVITE":
                self.wfile.write("SIP/2.0 100 Trying\r\n\r\n")
                print 'Enviando: ' + 'SIP/2.0 100 Trying\r\n\r\n'
                self.wfile.write("SIP/2.0 180 Ringing-\r\n\r\n")
                print 'Enviando: ' + 'SIP/2.0 180 Ringing\r\n\r\n'
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                print 'Enviando: ' + 'SIP/2.0 200 OK\r\n\r\n'
            elif method == "ACK":
                aEjecutar = ('./mp32rtp -i ' + IP + ' -p 23032 < ' + fich_audio)
                os.system(aEjecutar)
                print aEjecutar
            elif method == "BYE":
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                print 'Enviando: ' + 'SIP/2.0 200 OK\r\n\r\n'
            else:
                self.wfile.write("SIP/2.0 405 Method Not Allowed\r\n\r\n")
                print 'Enviando: SIP/2.0 405 Method Not Allowed\r\n\r\n'

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        serv = SocketServer.UDPServer((IP, PORT), SIPHandler)
    except (IndexError, ValueError):
        sys.exit("Usage: python servidor.py IP port audio_file")
    print "Listening...."
    serv.serve_forever()
