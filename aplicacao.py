#!/usr/bin/python3
# -*- coding: utf-8 -*

import sys
from protocolo import Subcamada

class Aplicacao(Subcamada):
    
    def __init__(self):
        Subcamada.__init__(self, sys.stdin)
  
    def recebe(self, dados:bytes):
      # mostra na tela os dados recebidos da subcamada inferior
      print('RX:', dados.decode())

    def handle(self):
      # lê uma linha do teclado
      dados = sys.stdin.readline()

      # envia os dados para a subcamada inferior (self.lower)
      self.lower.envia(dados.encode('utf8') )