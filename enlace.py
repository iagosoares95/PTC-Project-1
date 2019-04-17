# -*- coding: utf-8 -*-
import poller
import serial
import framing
import session
from tun import Tun

class Enlace:

    def __init__(self,minbytes=0,maxbytes=1024,serialport,timeout,ip1,ip2):
        self.mini_bytes=minbytes=0
        self.max_bytes=maxbytes=1024
        self.time=timeout
        self.ser=serial.Serial(serialport,9600,timeout=self.time)
        self.fra=fra.Framing(self.ser,self.time)
        self.pol=poller.Poller()
        self.tun=Tun("obj1",ip1,ip2,mask="255.255.255.252",mtu="1030",qlen="3")
        self.tun.start()
        #self.cal=cal.Callback(self,,1000)
        self.cb_tun=Callback_serial(self)
        self.cb_timer=Callback_tun()
        self.cb_serial=Callback
        self.pol.adiciona()

    def send(self,data):

    def receive(self):

class Callback_serial:

    def __init__(self,enl):

class Callback_tun:

    def __init__(self):

class Callback_timer:

    def __init__(self):

