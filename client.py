#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple

# Errores en la línea de comando
if len(sys.argv) != 3:
    print "Usage: python client.py method receiver@IP:SIPport"
    raise SystemExit

# METODO, LOGIN e IP del receptor
METODO = sys.argv[1].upper()
LOGIN = sys.argv[2].split("@")[0]
IP = sys.argv[2].split("@")[1].split(":")[0]

# Errores en los valores: METODO y PUERTO
metodos_SIP = ("INVITE", "BYE")

if not METODO in metodos_SIP:
    print "Error: Método SIP incorrecto"
    raise SystemExit

try:
    PUERTO = int(sys.argv[2].split("@")[1].split(":")[1])
except ValueError:
    print "Error: Puerto incorrecto"
    raise SystemExit
except IndexError:
    print "Usage: python client.py method receiver@IP:SIPport"
    raise SystemExit

# Contenido que vamos a enviar
LINE = METODO + " sip:" + LOGIN + "@" + IP + " SIP/2.0" + "\r\n"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PUERTO))

print "\nEnviando: " + LINE
my_socket.send(LINE + '\r\n')

# Error si el servidor no está lanzado
try:
    data = my_socket.recv(1024)
except socket.error:
    print "Error: No server listening at " + IP + " port " + str(PUERTO)
    raise SystemExit

print 'Recibido -- ', data

data_serv = data.split('\r\n\r\n')

# Si le ha enviado un INVITE y recibe esos códigos, envía el ACK
if METODO == 'INVITE' and \
    data_serv[0] == 'SIP/2.0 100 TRYING' and \
        data_serv[1] == 'SIP/2.0 180 RING' and \
            data_serv[2] == 'SIP/2.0 200 OK':
                LINE = "ACK sip:" + LOGIN + "@" + IP + " SIP/2.0\r\n"
                print "Enviando: " + LINE
                my_socket.send(LINE + '\r\n')
# Si le ha enviado un BYE y recibe ese código, se finaliza la conexión
elif METODO == 'BYE' and \
    data_serv[0] == 'SIP/2.0 200 OK':
        print "Se cierra la conexión con el servidor...\r\n"

# Cerramos el socket
print "Terminando socket..."
my_socket.close()
print "\nFin.\r\n"
