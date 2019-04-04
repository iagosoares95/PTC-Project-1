# -*- coding: utf-8 -*-
import framing
import enlace
from enum import Enum
import select

class Arq:

    def __init__(self,fra,timeout):
        self.events=Enum('Events','payload frame timeout')
        self.states=Enum('States','idle processing')
        self.state=self.states.
        self.fra=fra
        self.event=None
        self.timeout=timeout
        self.senddat=bytearray()
        self.data=bytearray()
        self.buffer=bytearray()


    def send(self,data):

    def receive(self):
        while(true):

    def handle_formats(self,event):
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

