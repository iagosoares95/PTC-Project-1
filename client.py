# -*- coding: utf-8 -*-
import enlace
import sys

if(len(sys.argv)<5):
    print('Exemplo de uso: client1.py /dev/pts/1 2 3 10.0.0.1 10.0.0.2')
    sys.exit(0)

port=sys.argv[1]
session_id=int(sys.argv[2])
timeout=float(sys.argv[3])
my_ip=sys.argv[4]
other_ip=sys.argv[5]

sessionid = int(sys.argv[2])
if(sessionid < 0 or sessionid > 255):
    print("O número da sessão deve ficar entre 0 e 255.")
    sys.exit(0)

enl=enlace.Enlace(port,timeout,my_ip,other_ip,session_id)
