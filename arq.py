#!/usr/bin/python3

import framing
from enum import Enum

class Arq:
    def __init__(self, framing):
        self.fra = framing
        self.States = Enum('States', 'idle waiting')
        self.state = self.States.idle
        self.Eventtype = Enum('EventType', 'payload frame timeout')

    def send(self, data):
        self.fra.send()

    def receive(self):
        self.fra.received()

    def handle(self):
        if(self.state == self.States.idle):

        elif(self.state == self.States.waiting):