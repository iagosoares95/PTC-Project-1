#!/usr/bin/python3
# -*- coding: utf-8 -*

from protocolo import Subcamada
from enum import Enum

class Eventos(Enum):
    CR = 1
    CC = 2
    DR = 3
    DC = 4
    TOUT = 5
    EDATA = 6
    RDATA = 7
    _CR = 8
    _DR = 9

class Sessao(Subcamada):

    def __init__(self, id_sessao, timeout):
        Subcamada.__init__(self, None, timeout)
        self.Estados = Enum('Estados', 'DISC ESP HALF1 HALF2 CONN')
        self.estado = self.Estados.DISC
        self.evento = None
        self.byte_sessao = bytearray()
        self.id_sessao = id_sessao
        self.rec_dado = bytearray()
        self.env_dado = bytearray()
        self.enable_timeout()
        self.ctrlbyte = bytearray()
        self.nkeepalive = 0

    def handle(self):
        if(self.estado == self.Estados.DISC):
            if(self.evento == Eventos._CR):
                self.estado = self.Estados.ESP
                self.ctrlbyte = b'\x01'
                self.lower.envia(self.ctrlbyte + bytes([self.id_sessao]) +b'\x01')
            if(self.evento == Eventos.CR):
                self.estado = self.Estados.CONN
                self.ctrlbyte = b'\x01'
                #self.timeout = 10
                self.nkeepalive = 0
                self.lower.envia(self.ctrlbyte + bytes([self.id_sessao]) + b'\x02')
                print("Conectado")
            if(self.evento == Eventos.EDATA):
                self.connecta()
        if(self.estado == self.Estados.ESP):
            if(self.evento == Eventos.CC):
                self.estado = self.Estados.CONN
                #self.timeout = 10
                print("Conectado")
                if(self.env_dado):
                    self.ctrlbyte = b'\x00'
                    self.lower.envia(self.ctrlbyte + bytes([self.id_sessao]) + b'\x00' + self.env_dado)
                    self.env_dado = bytearray()
        if(self.estado == self.Estados.CONN):
            if(self.evento == Eventos.DR):
                self.ctrlbyte = b'\x01'
                self.estado = self.Estados.HALF2
                self.lower.envia(self.ctrlbyte + bytes([self.id_sessao]) +b'\x03')
            if(self.evento == Eventos._DR):
                self.ctrlbyte = b'\x01'
                self.estado = self.Estados.HALF1
                self.lower.envia(self.ctrlbyte + bytes([self.id_sessao]) +b'\x03')
            if(self.evento == Eventos.EDATA):
                self.lower.envia(self.ctrlbyte + bytes([self.id_sessao]) + b'\x00' + self.env_dado)
                self.env_dado = bytearray()
            if(self.evento == Eventos.RDATA):
                if(len(self.rec_dado) > 1):
                    self.upper.recebe(self.rec_dado)
            if(self.evento == Eventos.TOUT):
                self.ctrlbyte = b'\x00'
                self.lower.envia(self.ctrlbyte + bytes([self.id_sessao]) + b'\x00')
        if(self.estado == self.Estados.HALF1):
            if(self.evento == Eventos.DR):
                self.ctrlbyte = b'\x01'
                self.lower.envia(self.ctrlbyte + bytes([self.id_sessao]) +b'\x04')
                self.estado = self.Estados.DISC
                print("Desconectado")
        if(self.estado == self.Estados.HALF2):
            if(self.evento == Eventos.DC):
                self.estado = self.Estados.DISC
                print("Desconectado")

    def connecta(self):
        self.nkeepalive = 0
        self.evento = Eventos._CR
        self.handle()

    def envia(self, payload):
        self.env_dado =  payload
        self.ctrlbyte = b'\x00'
        self.evento = Eventos.EDATA
        self.handle()

    def recebe(self, dados:bytes):
        ctrl = dados[0:1]
        ctrl_int = int.from_bytes(ctrl, "big")
        if((ctrl_int >> 7) & 1):
            self.nkeepalive = 0
            self.reload_timeout()
        ctrl_int = int.from_bytes(ctrl, "big")    
        ev = dados[2:3]
        self.rec_dado = dados[3:]
        if(int.from_bytes(dados[1:2] , "big") == self.id_sessao):
            self.nkeepalive = 0
            self.reload_timeout()
            if((ctrl_int % 2) == 1):
                if(ev == b'\x01'):
                    self.evento = Eventos.CR
                    print("CR recebido")
                if(ev == b'\x02'):
                    self.evento = Eventos.CC
                    print("CC recebido")
                if(ev == b'\x03'):
                    self.evento = Eventos.DR
                    print("DR recebido")
                if(ev == b'\x04'):
                    self.evento = Eventos.DC
                    print("DC recebido")
            else:
                self.evento = Eventos.RDATA
            self.handle()

    def handle_timeout(self):
        print('Sessão: Timeout')
        self.evento = Eventos.TOUT
        self.nkeepalive += 1
        if((self.nkeepalive == 3) and (self.estado == self.Estados.CONN)):
            self.estado = self.Estados.DISC
            print("Desconectado")
            self.disable_timeout()
        self.handle()