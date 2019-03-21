# -*- coding: utf-8 -*-
from enum import Enum

class framing:
    def __init__(self,porta,minbytes=0,maxbytes=256):
        self.porta=porta
        self.minbytes=minbytes
        self.maxbytes=maxbytes
        self.state=Enum('States','idle rx esc')
        self.estado=self.state.idle

    def send(self,msg):
        self.serial.write(msg)

    def receive(self):
        while(true):
            byte=self.serial.read()


    def handlei(self,received):
        if(self.estado==self.state.idle):
            self.estado=self.waiting(received)
            return false

        if(self.estado==self.state.rx):
            self.estado=self.reception(received)
            return false

        if(self.estado==self.state.esc):
            self.estado=self.escape(received)
            return false

    def waiting(self,received):
		
    def reception(self,received):

    def escape(self,received):
        if(self.received == )

    def xor(self,received):
        received1=received^0x20
        return received
