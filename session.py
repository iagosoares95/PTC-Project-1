# -*- coding: utf-8 -*-

import arq
import enlace
from enum import Enum
import time 

class Session:

    def __init__(elf,arq,timeout):
        self.States=Enum('States', 'disc hand1 hand2 con check half1 half2')
        self.states=self.States.disc
        self.arq=arq
        self.timeout=timeout
        self.max_no_resp=3
        self,send_data=bytearray()
        self.proto=b'\xff'
        self.CR=b'\x00'
        self.CC=b'\x01'
        self.received_data=bytearray()
        self.begin_conex=False
        self.send_time=time.time()

        def start(self):
            if(not(self.states in [self.States.disc,self.States.disc,self.States.disc]) and (self.begin_conex==True)):
                return
            self.states=self.States.disc
            self.begin_conex=True
            self.handle()


        def ends(self):

        def send(self):

        def receive(self):
            self.received_data=self.arq.receive()
            if(self.handle(self)==False)

        def timeout_func(self):

        def send_CR(self):
            self.send_data=bytearray()
            self.send_data=self.proto+self.CR
            self.arq.send(self.send_data)
            self.states=self.States.hand1

        def disc_func(self):
            if(begin_conex==True):
                print('Iniciando conexão')
                self.send_CR()
                self.send_time=time.time()
                return self.States.hand1
            else:
                if():

        def hand1_func(self):
            if(self.received_data[2:3]==self.CC[0:1]):
                print('Conexão estabelecida, CC recebido')
                return self.States.con
            return self.States.hand1

        def hand2_func(self):


        def handle(self):
            if(self.states==self.States.disc):
                self.states=self.disc_func()
                return False
            if(self.states==self.States.hand1):
                self.states=self.hand1_func()
                return False
            if(self.states==self.States.hand2):
                self.states=self.hand2_func()
                return False
