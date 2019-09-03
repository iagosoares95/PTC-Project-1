#!/usr/bin/python3
# -*- coding: utf-8 -*

import framing
import serial
import sys

if(len(sys.argv) < 2):
    print('Informe a porta serial.')
    print('Ex: client.py <client_type > /dev/pts/1')
    print('client_type:')
    print('s -> para o emissor')
    print('r -> para o receptor')
    exit()

client_type = sys.argv[1]
serial_port = sys.argv[2]
data = "abcedf1234567"

ser = serial.Serial(serial_port, 9600)
fra = framing.Framing(serial)
fra.send(data)