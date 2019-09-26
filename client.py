#!/usr/bin/python3
# -*- coding: utf-8 -*

import sys
import link

if(len(sys.argv) < 4):
    print('Informe o tipo de cliente(s -> para o emissor, r -> para o receptor), porta serial, ip do dispositivo e ip do dispositivo que se deseja comunicar.')
    print('Ex: client.py <client_type> /dev/pts/1 10.0.0.1 10.0.0.2')
    print('client_type:')
    exit()

client_type = sys.argv[1]
serial_port = sys.argv[2]
ip1 = sys.argv[3]
ip2 = sys.argv[4]
data = "abcedf~1234567"

l = link.Link(serial_port, ip1, ip2, client_type)