#!/usr/bin/python3
# -*- coding: utf-8 -*

from protocolo import Subcamada
from enum import Enum

class ARQ(Subcamada):

    def __init__(self, timeout):
        Subcamada.__init__(self, None, timeout)
        self.enable_timeout()
        self.Estados = Enum('Estados', 'ocioso espera')
        self.estado = self.Estados.ocioso
        self.Eventos = Enum('Eventos', 'ack dado payload timeout')
        self.evento = None
        self.buffer = bytearray()
        self.n_tentativas = 0
        self.seq_R = b'\x00'
        self.seq_E = False
        self.dado = bytearray()
        self.env_dado = bytearray()
        self.ctrlbyte = bytearray()
        self.id_sessao = bytearray()

    def envia(self, payload):
        self.evento = self.Eventos.payload
        self.buffer = payload[1:]
        self.ctrlbyte = payload[0:1]
        self.handle()

    def recebe(self, dados: bytes):
        self.evento = None
        self.dado = dados
        ctrl = dados[0:1]
        self.id_sessao = dados[1:2]
        ctrl_int = int.from_bytes(ctrl, "big")
        if((ctrl_int >> 7) & 1):
            self.evento = self.Eventos.ack
            self.buffer == bytearray()
        else:
            if((ctrl_int << 1) & 16):
                self.seq_R = 0x08
            else:
                self.seq_R = 0x00
            self.evento = self.Eventos.dado
        self.handle()

    def handle(self):
        if(self.estado == self.Estados.ocioso):
            if(self.evento == self.Eventos.payload):
                self.estado = self.Estados.espera
                self.envia_quadro()
                self.reload_timeout()
                self.enable_timeout()
            elif(self.evento == self.Eventos.dado):
                self.envia_ack()  
                self.upper.recebe(bytes(self.dado))            
                self.evento = None
        if(self.estado == self.Estados.espera):
            if(self.evento == self.Eventos.ack):
                print("ACK recebido")
                self.disable_timeout()
                self.estado = self.Estados.ocioso
                self.upper.recebe(bytes(self.dado))
            elif(self.evento == self.Eventos.dado):
                self.evento = None
                self.envia_ack()         
                self.upper.recebe(bytes(self.dado))
            elif(self.evento == self.Eventos.timeout):  
                self.n_tentativas += 1
                if(self.n_tentativas < 3):
                    self.envia_quadro()
                    self.reload_timeout()
                else:
                    self.estado = self.Estados.ocioso
                    self.n_tentativas = 0
                    self.disable_timeout()

    def handle_timeout(self):
        print('ARQ: Timeout')
        self.evento = self.Eventos.timeout
        self.handle()

    def envia_quadro(self):
        if(self.seq_E):
            controle = b'\x08'
        else:
            controle = b'\x00'
        self.seq_E = not self.seq_E
        controle_final = int.from_bytes(controle, byteorder="big") | int.from_bytes(self.ctrlbyte, byteorder="big")
        self.env_dado = bytes([controle_final]) + self.buffer
        self.lower.envia(self.env_dado)
        
    def envia_ack(self):
        if(self.seq_R == 8):
            ctrl = b'\x88'
        else:
            ctrl = b'\x80'
        self.lower.envia(ctrl + self.id_sessao + b'\x00')
        self.evento = None
