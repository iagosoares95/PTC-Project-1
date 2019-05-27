# -*- coding: utf-8 -*-
import framing
from enum import Enum
import select
import time

class Arq:

    def __init__(self,fra,timeout,session_id):
        self.Events=Enum('Events','payload frame timeout')
        self.States=Enum('States','idle processing')
        self.state=self.States.idle
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
        self.time_send=time.time()
        self.data=bytearray()

    def send(self,data):
        if(data==bytearray()):
            print('Informação a ser enviada: 0')
            return
        self.event=self.Events.payload
        self.data=bytearray()
        self.data=data
        self.handle(self.event)
        return

    def receive(self):
        self.data_received=bytearray()
        self.data_received=self.fra.receive()
        if(self.data_received==bytearray()):
            print('Nada foi recebido')
            return bytearray()
        self.event=self.Events.frame
        self.handle(self.event)
        return self.data_received

    def handle(self,event):
        if(self.state==self.States.idle):
            self.state=self.idle_func(event)
            return self.state
        elif(self.state==self.States.processing):
            self.state=self.processing_func(event)
            return self.state

    def idle_func(self,event_received):
        if(event_received==self.Events.frame):
            self.frame_func()
            return self.state
        elif(event_received==self.Events.payload):
            if(self.nbe==0):
                self.nbe=1
            else:
                self.nbe=0
            return self.make_frame()

    def processing_func(self,event_received):
        if(event_received==self.Events.frame):
            return self.frame_func()
        elif(event_received==self.Events.payload):
            self.data_received=self.fra.receive()
            self.frame_func()
            if(self.data_received!=bytearray()):
                return self.make_frame()
            return self.state
        return self.States.processing

    def make_ack(self,param):
        ack=bytearray()
        ctrl=0b10000000
        if(param==1):
            ctrl=0b10001000

        ack=bytes([ctrl])+bytes([self.session_ID])
        self.fra.send(ack)

    def make_frame(self):
        ctrl=0b00000000
        if(self.nbe==1):
            ctrl=0b00001000
            self.nbe=0
        else:
            self.nbe=1

        self.data_send=bytearray()
        self.data_send=self.data_send+bytes([ctrl])+bytes([self.session_ID])+self.data
        self.fra.send(self.data_send)
        print('Arq enviando:',self.data_send)
        self.time_send=time.time()
        return self.States.processing

    def frame_func(self):
        if(self.data_received==bytearray()):
            return self.state
        if((self.data_received[1:2]!=bytes([self.session_ID]))):
            print('Pacote recebido de outra sessão')
            self.data_received=bytearray()
            return self.state
        control=self.data_received[0]
        if(((control & 0b10000000)>>7)==1):
            if(((control & 0b00001000)>>3)==self.nbe):
                self.data_received=bytearray()
                return self.States.idle
        elif(((control & 0b10000000)>>7)==0):
            if(((control & 0b00001000)>>3)==self.nbr):
                self.make_ack(self.nbr)
                return self.state
            else:
                self.make_ack(self.nbr^1)
                return self.state
        
    def timeout_func(self):
        if(self.state==self.States.processing):
            time_diff=time.time()-self.time_send
            if(time_diff>self.timeout):
                self.make_frame()