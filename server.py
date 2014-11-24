#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor SIP en UDP simple
"""

import SocketServer
import sys
import os

NAME_PROGRAM = sys.argv[0]
IP = sys.argv[1]
PORT = int(sys.argv[2])
MP3 = sys.argv[3]
P_MP3 = str(23032)


class SipHandler(SocketServer.DatagramRequestHandler):
    """
    Sip server class
    """
    def handle(self):

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            metodo = line.split(" ")[0]
            ip_clnt = str(self.client_address[0])
            print line
            if metodo == "INVITE":
                self.wfile.write("SIP/2.0 100 Trying\r\n\r\n")
                self.wfile.write("SIP/2.0 180 Ringing\r\n\r\n")
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            elif metodo == "ACK":
                os.system('chmod 755 mp32rtp')
                run = './mp32rtp -i ' + ip_clnt + ' -p ' + P_MP3 + ' < ' + MP3
                os.system(run)
            elif metodo == "BYE":
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), SipHandler)
    print "listening...\r\n"
    serv.serve_forever()
