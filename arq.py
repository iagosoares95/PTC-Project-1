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
        self.time_send=time.time()

    def send(self,data):
        if(data==bytearray()):
            print('Informação a ser enviada: 0')
            return
        self.event=self.events.payload
        self.data_send=bytearray()
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

    def handle(self,event):
        if(self.state==self.states.idle):
            self.state=self.idle_func(event)
            return self.state
        elif(self.state==self.states.processing):
            self.state=self.processing_func(event)
            return self.state

    def idle_func(self,event_received):
        if(event_received==self.events.frame):
            self.frame_func()
            return self.state
        elif(event_received==self.events.payload):
            if(self.nbe==0):
                sel.nbe=1
            else:
                self.nbe=0
            return self.self.payload_func

    def processing_func(self,event_received):
        if(event_received==self.events.frame):
            return self.frame_func()
        elif(event_received==self.events.payload):

        return self.states.processing

    def make_ack(self,param):
        ack=bytearray()
        ctrl=0b10000000
        if(self.param==1):
            ctrl=0b10001000

        ack=bytes([ctrl])+bytes([self.session_ID])
        send.fra.envia(ack)

    def make_frame(self,param):
        ctrl=0b00000000
        if(self.param==1):
            ctrl=0b00001000
            self.nbr=0
        else:
            self.nbr=1

        data_send=bytes([ctrl])+bytes([session_ID])+self.data_send
        self.fra.send(data_send)
        self.time_send=time.time()
        return self.states.processing

    def frame_func(self):
        if(self.data_received[1:2]!=self.session_ID):
            print('Pacote recebido de outra sessão')
            self.data_received=bytearray()
            return self.state
        control=data_received[0]
        if(((control & 0b10000000)>>7)==1):
            if(((control & 0b00001000)>>3)==self.nbe):
                self.data_received=bytearray()
                return self.states.idle
        elif(((control & 0b10000000)>>7)==0):
            if(((control & 0b00001000)>>3)==self.nbr):
                self.make_ack(self.nbr)
                return self.state
            else:
                self.make_ack(self.nbr^1)
                return self.state
        
    def timeout_func(self):
        if(seld.state==self.states.processing):
            time_diff=time.time()-self.time_send
            if(time_diff>self.timeout):
                self.make_frame()
