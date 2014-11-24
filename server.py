#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# Roger Urrutia Bayo
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    def handle(self):
        # Recibimos del cliente
        x = True
        while x:
            line = str(self.rfile.read())
            # Separa lo recibido
            metodo = line.split(' ')[0]
            nick = line.split('sip:')[1].split('@')[0]
            IP = line.split('@')[1].split(' ')[0]
            print 'Recibo: ' + metodo + ' de ' + nick
            if metodo == 'INVITE':
                #Mando las respuestas al INVITE
                self.wfile.write("SIP/2.0 100 Trying\r\n")
                self.wfile.write("SIP/2.0 180 Ring\r\n")
                self.wfile.write("SIP/2.0 200 OK\r\n")
                self.wfile.write("\r\n")
                print 'Respondemos al INVITE de ' + nick
            elif metodo == 'ACK':
                #Al recibir el ACK ejecuto mp32rtp para mandar el fichero
                aEjecutar = ('./mp32rtp -i 127.0.0.1 -p 23032 < ' + f_audio)
                print "Ejecutando: ", aEjecutar
                os.system("chmod +x mp32rtp")
                os.system(aEjecutar)
            elif metodo == 'BYE':
                #Mando la confirmacion de haber recibido el BYE
                self.wfile.write("SIP/2.0 200 OK\r\n")
                print 'Enviamos OK a ' + nick
            else:
                #Respuestas de error
                self.wfile.write("SIP/2.0 400 Bad Request\r\n")
                self.wfile.write("SIP/2.0 405 Method Not Allowed\r\n")
                print 'Envio error a ' + nick
            x = False
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        #Comprobamos que se meten bien los parametros
        server = sys.argv[1]
        puerto = int(sys.argv[2])
        f_audio = sys.argv[3]
    except IndexError:
        print 'Usage: python servidor.py IP port audio_file'
        sys.exit()
    serv = SocketServer.UDPServer(("", puerto), EchoHandler)
    print "Listening..."
    serv.serve_forever()
