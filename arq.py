# -*- coding: utf-8 -*-
import framing
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
        self.data_send=bytearray()
        self.buffer=bytearray()
        self.nbe=0
        self.nbr=0
        self.ctrl_received=bytearray()
        self.data_received=bytearray()
        self.session_ID=session_id

    def send(self,data):
        if(data==bytearray()):
            print('Informação a ser enviada: 0')
            return
        self.event=self.events.payload
        self.data_send=data
        self.handle_events(self.event)
        return

    def receive(self):
        self.data_received=bytearray()
        self.data_received=self.fra.recebe()
        if(self.data_received==bytearray()):
            print('Nada foi recebido')
            return bytearray()
        self.event=sel.events.frame()
        self.handle(self.events)
        return self.data_received

    def handle_events(self,event):
        if(event==self.events.payload):
            self.data_received=bytearray()
            self.data=self.fra.recebe()
            if(len(self.data_received)==0):
                return self.
            self.frame_func()
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

    def frame_func(self):
        if(self.data_received[1:2]!=self.session_ID):
            print('Pacote recebido de outra sessão')
            self.data_received=bytearray()
            return self.state.idle
        control=data_received[0]
        if(((control & 0b10000000)>>7)==1):
        
    def timeout_func(self):
