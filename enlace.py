# -*- coding: utf-8 -*-
import poller
import serial
import framing
import arq
import session
from tun import Tun

class Enlace:

    def __init__(self,serial_port,timeout,ip1,ip2,session_id,maxbytes=1024):
        self.max_bytes=maxbytes=1024
        self.time=timeout
        self.ser=serial.Serial(serial_port,9600,timeout=self.time)
        self.fra=framing.Framing(self.ser,self.time)
        self.arq=arq.Arq(self.fra,self.time,session_id)
        self.se=session.Session(self.arq,self.time)
        self.pol=poller.Poller()
        if(ip1[-1]<ip2[-1]):
            self.tun=Tun("obj1",ip1,ip2,mask="255.255.255.252",mtu=1030,qlen=4)
        else:
            self.tun=Tun("obj2",ip1,ip2,mask="255.255.255.252",mtu=1030,qlen=4)
        self.tun.start()
        #self.cal=cal.Callback(self,,1000)
        self.callback_tun=Callback_tun(self.tun,self)
        self.callback_timer=Callback_timer(self,0.05)
        self.callback_serial=Callback_serial(self)
        self.pol.adiciona(self.callback_tun)
        self.pol.adiciona(self.callback_timer)
        self.pol.adiciona(self.callback_serial)
        sel.pol.despache()

    def send(self,data):
        if(self.se.state()!=con):
            self.se.start
        print('Enviando: %s' % data)
        self.se.send(data)
        return

    def receive(self):
        data_received=self.se.recebe()
        if((type(data_received)==bytearray) and (data_received!=bytearray())):
            print('Pacote recebido: %s' % data_received)
            self.tun.send_frame(data_received,Tun.PROTO_IPV4)

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
        if(self.enl.fra.validation(data_received)==True):
            self.enl.receive()

class Callback_tun(poller.Callback):

    def __init__(self,tun,enl):
        poller.Callback(tun.fd,1000)
        self.tun=tun
        self.enl=enl

    def handle_timeout(self):
        print("Timeout!")

    def handle(self):
       proto,data=self.tun.get_frame()
       self.enl.envia(data)

class Callback_timer(poller.Callback):

    def __init__(self,enl,timeout):
        poller.Callback(None,timeout)
        self.enl=enl

    def handle_timeout(self):
        self.enl.timeout_func()
