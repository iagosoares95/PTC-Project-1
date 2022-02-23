#!/usr/bin/python3
# -*- coding: utf-8 -*

import sys
from binascii import unhexlify
import poller
from enquadramento import Enquadramento
from aplicacao import Aplicacao
from serial import Serial
from arq import ARQ
from sessao import Sessao
#from interface_tun import NetTun

# nome da porta serial informada como primeiro argumento
# de linha de comando
ser = Serial(sys.argv[1])

enq = Enquadramento(ser, 10)

app = Aplicacao()

arq = ARQ(2)

ses = Sessao(1, 10)

#tun = NetTun()

# Conecta as subcamadas
# Deve ser feito a partir da subcamada inferior
enq.conecta(arq)

arq.conecta(ses)

ses.conecta(app)

#ses.conecta(tun)

# cria o Poller e registra os callbacks
sched = poller.Poller()
sched.adiciona(enq)
sched.adiciona(arq)
sched.adiciona(ses)
sched.adiciona(app)
#sched.adiciona(tun)

# entrega o controle ao Poller
sched.despache()