# -*- coding: utf-8 -*-
from enum import Enum
import crc
from binascii import unhexlify
import time

class Framing:

    def __init__(self,serial,timeout,minbytes=0,maxbytes=1024):
        self.serial=serial
        self.min_bytes=minbytes
        self.max_bytes=maxbytes
        self.States=Enum('States','idle rx esc')
        self.state=self.States.idle
        self.message=bytearray()
        self.frame_d=0
        self.max_bytes=1024
        self.fcs=crc.CRC16('')
        self.message_verified=bytearray()
        self.send_time=time.time()

    def send(self,msg):
        finalmsg=bytearray()
        sendmsg=bytearray()

        fcs=crc.CRC16(msg)
        msgcrc=fcs.gen_crc()

        for i in range (0,len(msgcrc)):
            if((msgcrc==0x7E) or (msgcrc==0x7D)):
                finalmsg=finalmsg+b'\x7D'+bytes([self.xor(msgcrc[i])])
            else:
                finalmsg=finalmsg+bytes([msgcrc[i]])

        sendmsg=b'\x7E'+finalmsg+b'\x7E'

        self.serial.write(sendmsg)

    def receive(self,received):
        msgreceived=self.message_verified
        self.message_verified=bytearray()
        return msgreceived

    def handle(self,received):
        if(self.state==self.States.idle):
            self.state=self.waiting(received)
            return False

        elif(self.state==self.States.rx):
            self.state=self.reception(received)
            if(self.state==self.States.idle):
                return True
            return False

        elif(self.state==self.States.esc):
            self.state=self.escape(received)
            return False

    def waiting(self,received):
        if(received==b'\x7E'):
            self.message=bytearray()
            return self.States.rx
        else:
            return self.States.idle
		
    def reception(self,received):
        self.send_time=time.time()
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
        self.send_time=time.time()
        if(received==b'\x7E' or received==b'\x7E'):
            self.message=bytearray()
            return self.States.idle
        else:
            correct_msg=self.xor(received[0])
            self.message=self.message+bytes([correct_msg])
            return self.States.rx

    def xor(self,received):
        received1=received^0x20
        return received1

    def timeout_func(self):
        if(self.state in [self.States.rx, self.States.esc]):
            time_diff=time.time()-self.send_time
            if(time_diff>timeout):
                self.message=bytearray()
                return self.States.idle

    def validation(self,received):
        if(self.handle(received)==True):
            data=self.message
            self.fcs.clear()
            self.fcs.update(data)
            crc_ok=self.fcs.check_crc()
            if(crc_ok==True):
                self.message_verified=data[0:-2]
                return True
            else:
                data=bytearray()
                return False
