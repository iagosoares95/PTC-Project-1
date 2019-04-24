# -*- coding: utf-8 -*-
import poller
import serial
import framing
import arq
import session
from tun import Tun

class Enlace:

    def __init__(self,minbytes=0,maxbytes=1024,serial_port,timeout,ip1,ip2,session_id):
        self.mini_bytes=minbytes=0
        self.max_bytes=maxbytes=1024
        self.time=timeout
        self.ser=serial.Serial(serial_port,9600,timeout=self.time)
        self.fra=framing.Framing(self.ser,self.time)
        self.arq=arq.Arq(self.fra,self.time,sessio_id)
        self.se=session.Session(self.arq,self.time)
        self.pol=poller.Poller()
        self.tun=Tun("obj1",ip1,ip2,mask="255.255.255.252",mtu="1030",qlen="4")
        self.tun.start()
        #self.cal=cal.Callback(self,,1000)
        self.cb_tun=Callback_serial(self)
        self.cb_timer=Callback_tun()
        self.cb_serial=Callback
        self.pol.adiciona()

    def send(self,data):

    def receive(self):

    def timeout_func(self):
        self.arq.timeout_func()
        self.fra.timeout_func()
        self.session.timeout_func()

class Callback_serial(poller.Callback):

    def __init__(self,enl):
        poller.Callback(enl.ser,1000)
        self.enl=enl
        self.serial1=enl.ser

    def handle_timeout(self):
        print("Timeout!")

    def handle(self):
        data_received=self.serial1.read()
        self.enl.enq.validation(data_received)

class Callback_tun(poller.Callback):

    def __init__(self,tun,enl):
        poller.Callback(tun.fd,1000)
        self.tun=tun
        self.enl=enl

    def handle_timeout(self):
        print("Timeout!")

    def handle(self):


class Callback_timer(poller.Callback):

    def __init__(self,enl,timeout):
        poller.Callback(None,timeout)
        self.enl=enl

    def handle_timeout(self):
        self.enl.timeout_func()
