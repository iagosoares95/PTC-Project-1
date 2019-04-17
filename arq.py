# -*- coding: utf-8 -*-
import framing
import enlace
from enum import Enum
import select

class Arq:

    def __init__(self,fra,timeout,session_id):
        self.events=Enum('Events','payload frame timeout')
        self.states=Enum('States','idle processing')
        self.state=self.states.idle
        self.fra=fra
        self.event=None
        self.timeout=timeout
        self.data=bytearray()
        self.buffer=bytearray()
        self.data=bytearray()
        self.nbe=0
        self.nbr=0
        self.ctrl_received=bytearray()
        self.data_received=bytearray()

    def send(self,data_received):
        if(data_received==bytearray()):
            print('Informação a ser enviada: 0')
            return
        self.event=self.events.payload
        self.data=data_received
        self.handle_events(self.event)

    def receive(self):
        self.data_received=self.fra.recebe()
        self.event=sel.events.frame

    def handle_events(self,event):
        if(event==self.events.payload):
            self.set_timeout()
        elif(event==self.events.frame):

        elif(event==self.events.timeout):

    def handle_states(self,state):
        if(self.state==self.states.idle):

        elif(self.state==self.states.processing):

    def set_timeout(self):

    def data_received(self):

    def make_ack(self):
        ack=bytearray()
        if(ctrl_received==)

    def make_frame(self):
        if(self.nbe==0):
            ctrl=0b00000000
            self.nbe=1
        else:
            ctrl=0b00001000
            self.nbe=0

        msgsend=bytes(ctrl)+self.data
        self.fra.send(msgsend)

    def timeout_func(self):
