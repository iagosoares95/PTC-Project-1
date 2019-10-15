#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum
import ARQ
import link

class Session:
    def __init__(self, arq):
        self.States = Enum('States', 'disc hand1 hand2 hand3 con check half1 half2')
        self.states = self.State.disc
        self.arq = arq
        self.CR = b'\x00'
        self.CC = b'\x01'
        self.KR = b'\x02'
        self.KC = b'\x03'
        self.DR = b'\x04'
        self.DC = b'\x05'
        self.start = False
        self.recv_data = bytearray()
        self.proto = b'\xff'
        self.s_data = bytearray()

    def begin(self):
        if(self.states == seld.States.con):
            return
        if(self.start == True):
            return
        self.states = self.States.disc
        self.start = True
        self.handle()
    
    def finish(self):
        self.DR_func()
        seld.states = self.States.half1

    def send(self):

    def receive(self):
        self.recv_data = self.arq.receive()
        if(self.handle() == False):

    def handle(self):
        if(self.states == self.States.disc):
            self.states = self.disc_func()
            return False
        elif(self.states == self.States.hand1):
            self.states = self.hand1_func()
            return False
        elif(self.states == self.States.hand2):
            self.states = self.hand2_func()
            return False
        elif(self.states == self.States.hand3):
            self.states = self.hand3_func()
            return False
        elif(self.states == self.States.con):
            self.states = self.con_func()
            return False
        elif(self.states == self.States.check):
            self.states = self.check_func()
            return False
        elif(self.states == self.States.half1):
            self.states = self.half1_func()
            return False
        elif(self.states == self.States.half2):
            self.states = self.half2_func()
            return False

    def disc_func(self):
        if(len(self.recv_data) == 0):
            return self.States.disc
        if(self.start == True):
            self.CR_func()
            return self.States.hand1
        else:
            if():

    def hand1_func(self):
        if(len(self.recv_data) == 0):
            self.CR_func()
            return self.States.hand1
        if()            

    def hand2_func(self):
        if(len(self.recv_data) == 0):
            return self.States.hand2
        if():           

    def hand3_func(self):

    def con_func(self):
        if(self.s_data != bytearray()):
            self.arq.send(s_data)
            return self.States.con
            
    def check_func(self):

    def half1_func(self):
        if(len(self.recv_data) == 0):
            self.DR_func()
            return self.States.half1
        if():

    def half2_func(self):
        if(len(self.recv_data) == 0):
            return self.States.disc
        if():

    def CR_func(self):
        send_data = self.proto + sel.CR
        self.arq.send(send_data)
    
    def DR_func(self):
        send_data = self.proto + self.DR
        self.arq.send(send_data)

    def timeout_func(self):