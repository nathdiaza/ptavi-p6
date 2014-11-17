#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
import os
# Cliente UDP simple.
NAME_PROGRAM = sys.argv[0]
METODO = sys.argv[1]
LOGIN = sys.argv[2].split("@")[0]
R_IP_PORT = sys.argv[2].split("@")[1]
IP = R_IP_PORT.split(":")[0]
PORT = R_IP_PORT.split(":")[1]

# Dirección IP del servidor.
SERVER = 'localhost'
PORT = 6001

# Contenido que vamos a enviar
LINE = '¡Hola mundo!'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + LINE
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
