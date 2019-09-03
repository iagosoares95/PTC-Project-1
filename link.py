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
        self.pol.despache()

    def send(self):

    def received(self):

class TunCallback(poller.Callback):
    def __init__(self, tun, link):
        poller.Callback.__init__(self, tun.fd)
        self.tun = tun
        self.enl = enl

    def 