#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os
class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class(INVITE,ACK y BYE)
    """

    def handle(self):

        while 1:
            line = self.rfile.read()
            if not line:
                break
            print line
            method = line.split(" ")[0]
            if method == "INVITE":
                self.wfile.write("SIP/2.0 100 Trying\r\n\r\n")
                self.wfile.write("SIP/2.0 180 Ring\r\n\r\n")
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            elif method == "ACK":
                aEjecutar = ('./mp32rtp -i ' + IP + ' -p 23032 < ' + \
                fich_audio)
                os.system(aEjecutar)
                print aEjecutar
                
            elif method == "BYE":
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            else:
                self.wfile.write("SIP/2.0 405 Method Not Allowed\r\n\r\n")

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    fich_audio = sys.argv[3]
    try:
        serv = SocketServer.UDPServer((IP, PORT), EchoHandler)
    except (IndexError, ValueError):
        sys.exit("Usage: python servidor.py IP port audio_file")
    print "Listening...."
    serv.serve_forever()
