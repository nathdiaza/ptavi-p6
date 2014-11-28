#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente SIP envia INVITE, BYE Y ack
"""

import socket
import sys


if len(sys.argv) != 3 or "@" not in sys.argv[2]:
    sys.exit("Usage: python cliente.py method receiver@IP:SIPport")

METHOD = sys.argv[1]
line = sys.argv[2]
SIP_ADDRES = line.split("@")[0]
line = line.split("@")[1]

if ":" not in line:
    sys.exit("Usage: python cliente.py method receiver@IP:SIPport")

SERVER = line.split(":")[0]
PORT = int(line.split(":")[1])

try:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))
    line = METHOD + " sip:" + SIP_ADDRES + "@" + SERVER + " SIP/2.0"
    print line
    my_socket.send(line + '\r\n\r\n')
    data = my_socket.recv(1024)
    print 'Recibido -- \r\n', data
    data = data.split("SIP/2.0 ")
    if "200 OK\r\n\r\n" in data and METHOD == "INVITE":
        line = "ACK sip:" + SIP_ADDRES + "@" + SERVER + " SIP/2.0"
        my_socket.send(line + '\r\n\r\n')
        print line
    my_socket.close()
except:
    print "Error: no server listening at " + SERVER + " port " + str(PORT)
