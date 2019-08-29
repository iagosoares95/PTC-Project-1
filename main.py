#!/usr/bin/python3

import framing

if(len(sys.argv) < 2):
    print('É necessário informar a porta serial')
    print('Ex: main.py /dev/pts/1')
    exit()