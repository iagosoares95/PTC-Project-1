# -*- coding: utf-8 -*-
import poller
import serial
import framing

class Enlace:

    def __init__(self,minbytes=0,maxbytes=1024,serialport,timeout):
        self.mini_bytes=minbytes=0
        self.max_bytes=maxbytes=1024
        self.time=timeout
        self.ser=serial.Serial(serialport,9600,timeout=self.time)
        self.fra=fra.Framing(self.ser,self.time)
        self.pol=poller.Poller()

    def send(self,data):

    def receive(self):
