# -*- coding: utf-8 -*-
import poller
import serial
import framing
from tun import Tun

class Enlace:

    def __init__(self,minbytes=0,maxbytes=1024,serialport,timeout,ip1,ip2):
        self.mini_bytes=minbytes=0
        self.max_bytes=maxbytes=1024
        self.time=timeout
        self.ser=serial.Serial(serialport,9600,timeout=self.time)
        self.fra=fra.Framing(self.ser,self.time)
        self.pol=poller.Poller()
        self.tun=Tun("obj1",ip1,ip2,)
        #self.cal=cal.Callback(self,,1000)
        self.
        self.pol.adiciona()

    def send(self,data):

    def receive(self):

    def callback_serial():

    def callback_tun():

    def callback_timer():

