#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys

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
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente nos manda " + line

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PUERTO), EchoHandler)
    print "\nLanzando servidor UDP de eco... \r\n"
    serv.serve_forever()
