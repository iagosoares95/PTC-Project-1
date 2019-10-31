#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum
import ARQ
import link
import time

class Session:
    def __init__(self, arq, timeout):
        self.States = Enum('States', 'disc hand1 hand2 hand3 con check half1 half2')
        self.states = self.States.disc
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
        self.l_time = time.time()
        self.timeout = timeout

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

    def conected(self):
        if(self.states == self.States.con):
            return True
        else: 
            return False

    def send(self, data):
        if(self.states != self.States.con):
            return 
        self.s_data = bytearray()
        self.s_data = self.proto + data

    def receive(self):
        self.recv_data = self.arq.receive()
        if(self.handle() == False):
            return self.recv_data
        else:
            return bytearray()

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
            if(self.states == self.States.disc):
                return True
            return False
        elif(self.states == self.States.half2):
            self.states = self.half2_func()
            if(self.states == self.States.disc):
                return True
            return False

    def disc_func(self):
        if(len(self.recv_data) == 0):
            return self.States.disc
        if(self.start == True):
            self.CR_func()
            self.l_time = time.time()
            return self.States.hand1
        else:
            if(len(self.recv_data) == 0):
                return self.States.disc
            if((self.recv_data[2:3] == self.proto[0:1]) and (self.recv_data[3:4] == self.CR[0:1])):
                print("Pedido de conexão recebido")
                self.s_data = bytearray()
                self.s_data = self.proto + self.CC
                print("Enviando CC")
                self.arq.send(self.s_data)
                return self.States.hand2
            return self.States.disc

    def hand1_func(self):
        if(len(self.recv_data) == 0):
            return self.States.hand1
        if(self.recv_data[3:4] == self.CC[0:1]):
            print("CC recebido")
            return self.States.hand3
        return self.States.hand1              

    def hand2_func(self):
        if(len(self.recv_data) == 0):
            return self.States.hand2
        if(self.):           

    def hand3_func(self):


    def con_func(self):
        if(self.s_data != bytearray()):
            self.arq.send(s_data)
            return self.States.con
        if(len(self.recv_data) != 0):
            if((self.recv_data[2:4] == self.proto[0:1]) and (self.recv_data[3:4] == self.DR[0:1])):
                print("Pedido de desconexão recebido")
                self.DR_func()
                return self.States.half2
            else:
                self.recv_data = self.recv_data[4:]
                return self.States.con
        return self.States.con
            
    def check_func(self):

    def half1_func(self):
        if(len(self.recv_data) == 0):
            return self.States.half1
        if(self.recv_data[3:4] == self.DR[0:1]):
            print("Confirmação de desconexão recebida")
            self.s_data = bytearray()
            self.s_data = self.proto + self.DC
            print("Enviando confirmaçãoo de desconexão")
            self.arq.send(self.s_data)
            return self.States.disc
        return self.States.half1

    def half2_func(self):
        if(len(self.recv_data) == 0):
            return self.States.disc
        if(self.recv_data[3:4] == self.DC[0:1]):
            print("Confirmação de desconexão recebida")
            return self.States.disc
        if(self.recv_data[3:4] == self.DR[0:1]):
            self.DR_func()
            return self.States.half2

    def CR_func(self):
        send_data = self.proto + sel.CR
        self.l_time = time.time()
        self.arq.send(send_data)
    
    def DR_func(self):
        send_data = self.proto + self.DR
        self.l_time = time.time()
        self.arq.send(send_data)

    def timeout_func(self):
        if(self.states == self.States.hand1):
            self.diff_time = time.time() - self.l_time
            if(diff_time > self.timeout):
                self.CR_func()
        if(self.states == self.States.hand2):
            self.diff_time = time.time() - self.l_time
            if(diff_time > self.timeout):
                self.states = self.States.disc
                self.start = False
        if(self.states == self.States.half1):
            self.diff_time = time.time() - self.l_time
            if(diff_time > self.timeout):
                self.DR_func()
        if(self.states == self.States.half2):
            self.diff_time = time.time() - self.l_time
            if(diff_time > self.timeout):
                self.states = self.States.disc