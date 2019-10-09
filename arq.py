#!/usr/bin/python3

import framing
from enum import Enum

class Arq:
    def __init__(self, framing):
        self.fra = framingz
        self.States = Enum('States', 'idle waiting')
        self.state = self.States.idle
        self.Eventtype = Enum('EventType', 'payload frame timeout')
        self.event = None
        self.buffer = bytearray()

    def send(self, data):
        if(data == bytearray()):
            return
        self.event = self.Eventtype.payload
        self.data = data
        self.handle_state(self.event)

    def receive(self):
        self.buffer = self.fra.received()
        if(self.bufer == bytearray()):
            return bytearray()
        
        self.event = self.Eventtype.frame
        self.handle_state(self.event)
        return self.buffer

    def handle_state(self, event):
        if(self.state == self.States.idle):
            self.state = self.idle_func(event)
            return self.state
        elif(self.state == self.States.waiting):
            self.state = self.waiting_func(event)
            return self.state

    def idle_func(self, event):
        if(self.event == self.Eventtype.payload):
        
        elif(self.event == self.Eventtype.frame):

    def waiting_func(self, event):        
        if(self.event == self.Eventtype.payload):
        
        elif(self.event == self.Eventtype.frame):