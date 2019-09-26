#!/usr/bin/python3

from tun import Tun
import framing
import serial
import poller

class Link:
    def __init__(self, serial_port, ip1, ip2, client_type):
        self.serial = serial.Serial(serial_port, 9600)
        self.fra = framing.Framing(self.serial)
        self.tun = Tun("tun1", ip1, ip2, mask="255.255.255.252", mtu=1500, qlen=4)
        self.tun.start()
        self.pol = poller.Poller()
        if(client_type == "s"):
            self.tun_callback = TunCallback(self.tun,self)
            self.pol.adiciona(self.tun_callback)
        self.serial_callback = SerialCallback(self)
        self.pol.adiciona(self.serial_callback)
        self.pol.despache()

    def send(self, data):
        print("Dado: ", data)
        self.fra.send(data)

    def received(self):
        buffer = self.fra.receive()
        if((type(buffer) == bytearray) and buffer != bytearray()):
            print('Pacote recebido:')
            print(buffer)
            self.tun.send_frame(buffer, Tun.PROTO_IPV4)

class TunCallback(poller.Callback):
    def __init__(self, tun, link):
        poller.Callback.__init__(self, tun.fd)
        self.tun1 = tun
        self.link = link

    def handle(self):
        proto, payload = self.tun1.get_frame()
        print("Lido: ", payload)
        self.link.send(payload)

class SerialCallback(poller.Callback):
    def __init__(self,link):
        poller.Callback.__init__(self, link.serial)
        self.link = link
        self.serial1 = link.serial

    def handle(self):
        recv_data = self.serial1.read()
        if(recv_data != bytearray()):
            self.serial1.read()