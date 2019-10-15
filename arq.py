#!/usr/bin/python3

import framing
from enum import Enum

class Arq:
    def __init__(self, framing, session__id):
        self.fra = framing
        self.States = Enum('States', 'idle waiting')
        self.state = self.States.idle
        self.Eventtype = Enum('EventType', 'payload frame timeout')
        self.event = None
        self.buffer = bytearray()
        self.ns_frame = 0
        self.session_id = session__id
        self.s_data = bytearray()

    def send(self, data):
        if(data == bytearray()):
            return
        self.event = self.Eventtype.payload
        self.s_data = data
        self.handle_state(self.event)
        return

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
            return self.make_payload()
        elif(self.event == self.Eventtype.frame):
            return self.frame_func()

    def waiting_func(self, event):        
        if(self.event == self.Eventtype.payload):
            self.buffer = self.fra.receive()
            if(self.buffer == bytearray()):
                return self.States.waiting
            return self.frame_func()        
        elif(self.event == self.Eventtype.frame):
            if(self.buffer == bytearray()):
                return self.States.idle
            return self.frame_func()
        reurn self.States.waiting

    def make_payload(self):
        ctrl = 0b00000000
        if(self.ns_frame = 1):
            ctrl = ctrl | 0b00001000
            self.ns_frame = 0
        else:
            self.ns_frame = 1

        send_data = bytes([ctrl]) + bytes([session_id]) + self.s_data
        self.fra.send(send_data)
        return self.States.waiting
        
    def frame_func(self):
        if():

    def make_ack(self):
        ack = bytes([ctrl]) + bytes([self.session_id])
        self.fra.send(ack)

    def timeout_func(self):