#!/usr/bin/python3
# -*- coding: utf-8 -*

from protocolo import Subcamada
from tun import Tun

class NetTun(Subcamada):
    
    def __init__(self, tun):
        Subcamada.__init__(self, tun.fd)
        self._tun = tun
        tun = Tun("tun0","10.0.0.1","10.0.0.2",mask="255.255.255.252",mtu=1500,qlen=4)
        self._tun.start()

    def handle(self):
        l = self._tun.get_frame()
        print('Lido:', l)
        self.lower.envia(l.encode('utf8') )
        
    def handle_timeout(self):
        print('Timeout !')