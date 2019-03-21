# -*- coding: utf-8 -*-
import enlace
import sys

if(len(sys.argv)<1):
    print('Entre com o endereço da port serial')
else:
    print('Dica: client1.py /dev/pts/1')
    exit()

porta=sys.argv[1]
e=enlace.Enlace(porta)

msg=input('Digite um dado para ser enviado:').encode('utf-8')
msg1=bytearray(msg)

e.send(msg1)
