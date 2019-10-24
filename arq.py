#!/usr/bin/python3
# -*- coding: utf-8 -*-

import framing
from enum import Enum
import time

class Arq:
    def __init__(self, framing, session_id, timeout):
        self.fra = framing
        self.States = Enum('States', 'idle waiting')
        self.state = self.States.idle
        self.Eventtype = Enum('EventType', 'payload frame timeout')
        self.event = None
        self.buffer = bytearray()
        self.ns_frame = 0
        self.nr_frame = 0
        self.session_id = session_id
        self.s_data = bytearray()
        self.timeout = timeout
        self.l_time = time.time()
        self.LimitRetries = 3
        self.maxLimitRetries = 3

    def send(self, data):
        if(data == bytearray()):
            return
        self.event = self.Eventtype.payload
        self.s_data = data
        self.handle_state(self.event)
        return

    def receive(self):
        self.buffer = self.fra.received()
        if(self.buffer == bytearray()):
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
        return self.States.waiting

    def make_payload(self):
        ctrl = 0b00000000
        if(self.ns_frame == 1):
            ctrl = ctrl | 0b00001000
            self.ns_frame = 0
        else:
            self.ns_frame = 1

        send_data = bytes([ctrl]) + bytes([self.session_id]) + self.s_data
        self.fra.send(send_data)
        self.l_time = time.time()
        self.LimitRetries = self.LimitRetries + 1
        return self.States.waiting
        
    def frame_func(self):
        if(self.buffer[1:2] != bytes([self.session_id])):
            print("Pacote recebido de sessão diferente")
            self.buffer = bytearray()
            return self.state
            if(((self.buffer[0] & 0b1000000) >> 7) == 1):
                if(((self.buffer[0] & 0b00001000) >> 3) == self.ns_frame):
                    print("Ack recebido")
                    self.LimitRetries = 0
                    self.l_time = time.time()
                    self.buffer = bytearray()
                    self.States.idle
                else:
                    print("Ack recebido de pacote diferente, reenviado pacote")
                    self.make_payload()
                    return self.States.waiting
        else:
            self.nr_frame = ((self.buffer[0] & 0b00001000) >> 3)
            self.make_ack()
            return self.state

    def make_ack(self):
        ack = bytearray()
        ctrl = 0b10000000
        if(self.nr_frame == 1):
            ctrl = ctrl | 0b00001000
        ack = bytes([ctrl]) + bytes([self.session_id])
        self.fra.send(ack)

    def timeout_func(self):
        if(self.state == self.States.waiting):
            diff_time = time.time() - self.l_time
            if(diff_time > self.timeout):
                if(self.LimitRetries > self.maxLimitRetries):
                    self.l_time = time.time()
                    self.LimitRetries = 0
                    self.state = self.States.idle
                    print("Número máximo de retransmissões alcançado")
                else:
                    print("Timeout Arq")
                    self.make_payload()