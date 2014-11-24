#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
import os

list_metodo = ['INVITE', 'BYE']

if len(sys.argv) != 3:
    print 'Usage: python client.py method receiver@IP:SIPport'
    raise SystemExit

if sys.argv[1] not in list_metodo:
    print 'Usage: python client.py method receiver@IP:SIPport'
    raise SystemExit

try:
    R_IP_PORT = sys.argv[2].split("@")[1]
    PORT = int(R_IP_PORT.split(":")[1])
except ValueError:
    print 'Usage: python client.py method receiver@IP:SIPport'
    raise SystemExit

METODO = sys.argv[1]
LOGIN = sys.argv[2].split("@")[0]
IP_SERVER = R_IP_PORT.split(":")[0]
# Contenido que vamos a enviar
LINE = METODO + " sip:" + LOGIN + "@" + IP_SERVER + " SIP/2.0\r\n\r\n"
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP_SERVER, PORT))

print "Enviando: " + LINE

try:
    my_socket.send(LINE + '\r\n')
    data = my_socket.recv(1024)

except socket.error:
    print 'Error: No server listening at ' + IP_SERVER + ' port ' + str(PORT)
    raise SystemExit

print 'Recibido -- \r\n\r\n', data

if METODO == "INVITE":
    if data.split("\r\n\r\n")[0] == "SIP/2.0 100 Trying":
        if data.split("\r\n\r\n")[1] == "SIP/2.0 180 Ringing":
            if data.split("\r\n\r\n")[2] == "SIP/2.0 200 OK":
                ack = "ACK sip:" + LOGIN + "@" + IP_SERVER + " SIP/2.0\r\n\r\n"
                my_socket.send(ack + "\r\n")

print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
