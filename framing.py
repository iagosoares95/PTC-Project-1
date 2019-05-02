# -*- coding: utf-8 -*-
from enum import Enum
import crc
from binascii import unhexlify

class Framing:

    def __init__(self,serial,minbytes=0,maxbytes=1024,timeout):
        self.serial=serial
        self.min_bytes=minbytes
        self.max_bytes=maxbytes
        self.state=Enum('States','idle rx esc')
        self.estado=self.state.idle
        self.message=bytearray()
        self.frame_d=0
        self.max_bytes=1024
        self.fcs=crc.CRC16()

    def send(self,msg):
        finalmsg=bytearray()
        sendmsg=bytearray()

        fcs=crc.CRC16(msg)
        msgcrc=fcs.gen_crc()

        for i in range (0,len(msgcrc)):
            if((msgcrc==0x7E) or (msgcrc==0x7D)):
                finalmsg=finalmsg+b'\x7D'+bytes([self._xor20(msgcrc[i])])
            else:
                finalmsg=finalmsg+bytes([msgcrc[i]])

        sendmsg=b'\x7E'+finalmsg+b'\x7E'

        self.serial.write(sendmsg)

    def receive(self,received):
        msgreceived=self.serial.read()
        self.handle(msgreceived)
        return msgreceived

    def handle(self,received):
        if(self.estado==self.state.idle):
            self.estado=self.waiting(received)
            return False

        elif(self.estado==self.state.rx):
            self.estado=self.reception(received)
            if(self.estado==self.state.ocioso):
                return True
            return False

        elif(self.estado==self.state.esc):
            self.estado=self.escape(received)
            return False

    def waiting(self,received):
        if(received==b'\x7E'):
            self.message=bytearray()
            return self.States.rx
        else:
            return self.States.idle
		
    def reception(self,received):
        if(received==b'\x7E'):
            self.frame_d=self.frame_d+1
            if(self.frame_d==2):
                self.frame_d=0
                return self.States.idle
            return self.States.rx
        elif(received!=b'\x7E' and received!=b'\x7D'):
            self.message=self.message+received
            if(len(self.message)>self.max_bytes):
                self.message=bytearray()
                return self.States.idle
            return self.States.rx
        elif(received==b'\x7D'):
            return self.States.esc

    def escape(self,received):
        if(received==b'\x7E' or received==b'\x7E'):
            return self.States.idle
        else:
            correcmsg=self.xor(received)

    def xor(self,received):
        received1=received^0x20
        return received1

    #def timeout_func(self):

    def validation(self,received):
        if(self.handle(received)==True):
            data=self.message
            self.fcs.clear()
            self.fcs.update(data)
            crc_ok=self.fcs.check_crc()
            if(crc_ok==True):
