#!/usr/bin/python3

from tun import Tun
import framing
import serial

class Link:
    def __init__(self, serial_port, ip1, ip2):
        self.serial = serial.Serial(serial_port, 9600)
        self.fra = framing.Framing(self.serial)
        self.tun = Tun("tun1", ip1, ip2, mask="255.255.255.252", mtu=1500, qlen=4)
        self.tun.start()
        self.pol = poller.Poller()
        self.tun_callback = TunCallback(self.tun,self)
        self.adiciona(self.tun.Callback)
        self.serial_callback = SerialCallback(self)
        self.adiciona(self.serial_callback)
        self.pol.despache()

    def send(self, data):
        self.fra.send(data)

    def received(self):
        buffer = self.fra.receive()
        if((type(buf)==bytearray) and buf!=bytearray()):
            print('Pacote recebido:')
            print(buffer)
            self.tun.send_frame(buffer, Tun.PROTO_IPV4)

class TunCallback(poller.Callback):
    def __init__(self, tun, link):
        poller.Callback.__init__(self, tun.fd)
        self.tun = tun
        self.lin = lin

    def handle()

class SerialCallback(poller.Callback):
    def __init__(self,link):
        poller.Callback.__init__(self, lin.ser)

    def handle(self):