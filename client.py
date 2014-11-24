#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# Roger Urrutia Bayo
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Obtenemos y comprobamos los datos pasados
try:
    metodo = sys.argv[1]
    usuario = sys.argv[2]

    # Sacamos la ip y el puerto del usuario
    receptor = usuario.split('@')[0]
    SERVER = usuario.split('@')[1].split(':')[0]
    PORT = int(usuario.split('@')[1].split(':')[1])
except IndexError:
    print 'Usage: python cliente.py method receiver@IP:SIPport'
    sys.exit()

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

# Enviamos el mensaje
print "Enviando " + metodo
linea = metodo + ' sip:' + receptor + '@' + SERVER
my_socket.send(linea + ' SIP/2.0' + '\r\n')

# Analizamos las respuestas del server
try:
    data = my_socket.recv(1024)
except socket.error:
    print 'Error: no server listening at ' + SERVER + ' port ' + str(PORT)
    sys.exit()

print 'Recibido: ' + data
#Separamos lo recibido para obtener el tipo de respuesta
respuesta = data.split("SIP/2.0 ")[1]
if respuesta == '100 Trying\r\n':
    #Mandamos ACK al servidor
    metodo = 'ACK'
    print "Enviando " + metodo
    linea = metodo + ' sip:' + receptor + '@' + SERVER
    my_socket.send(linea + ' SIP/2.0' + '\r\n')
elif respuesta == '200 OK\r\n':
    print "Salimos"
elif respuesta == '400 Bad Request\r\n':
    #Imprimimos el error
    print 'Error: ' + respuesta[1] + respuesta[2]

# Cerramos todo
my_socket.close()
print "Fin."
