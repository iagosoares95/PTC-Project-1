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
        self.received_data=bytearray()

        def start(self):

        def ends(self):

        def send(self):
            self.received_data=self.arq.receive()

        def receive(self):

        def timeout_func(self):

        def send_CR(self):
            self.send_data=bytearray()
            self.send_data=self.proto+self.CR
            self.arq.send(self.send_data)
            self.states=self.States.hand1

