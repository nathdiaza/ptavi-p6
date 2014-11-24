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
LINE = sys.argv[2]
SIP_ADDRES = LINE.split("@")[0]
LINE = LINE.split("@")[1]

if ":" not in LINE:
    sys.exit("Usage: python cliente.py method receiver@IP:SIPport")

SERVER = LINE.split(":")[0]
PORT = int(LINE.split(":")[1])

try:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))
    LINE = METHOD + " sip:" + SIP_ADDRES + "@" + SERVER + " SIP/2.0"
    print  LINE
    my_socket.send(LINE + '\r\n\r\n')
    data = my_socket.recv(1024)    
    print 'Recibido -- \r\n', data
    data = data.split("SIP/2.0 ")
    if "200 OK\r\n\r\n" in data and METHOD == "INVITE":
        LINE = "ACK sip:" + SIP_ADDRES + "@" + SERVER + " SIP/2.0"
        my_socket.send(LINE + '\r\n\r\n')
        print  LINE
    my_socket.close()
except:

    print "Error: no server listening at " + SERVER + " port " + str(PORT)
