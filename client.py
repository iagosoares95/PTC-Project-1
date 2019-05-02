# -*- coding: utf-8 -*-
import enlace
import sys

if(len(sys.argv)<5):
    print('Entre com o endereço da porta serial, número da sessão, tempo de timeout, seu ip e o ip do outro dispositivo')
else:
    print('Ex: client1.py /dev/pts/1 2 3 10.0.0.1 10.0.0.2')
    exit()

port=sys.argv[1]
session_id=int(sys.argv[2])
timeout=float(sys.argv[3])
my_ip=sys.argv[4]
other_ip=sys.argv[5]

enl=enlace.Enlace(port,session_id,timeout,my_ip,other_ip)
