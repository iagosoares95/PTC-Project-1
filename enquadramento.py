#!/usr/bin/python3
# -*- coding: utf-8 -*

from enum import Enum
from protocolo import Subcamada
import crc

class Enquadramento(Subcamada):

    def __init__(self, serial, timeout):
        Subcamada.__init__(self, serial, timeout)
        self.Estados = Enum('Estados', 'ocioso init rx esc')
        self.estado = self.Estados.ocioso
        self.buffer = bytearray()
        self.n_bytes = 0
        self.ser = serial
        self.enable_timeout()

    def envia(self, data):
        final_data = bytearray()
        fcs = crc.CRC16(data)
        data_crc = fcs.gen_crc()
        for i in range(0, len(data_crc)):
            if((data_crc[i] == 0x7E) or (data_crc[i] == 0x7D)):
                trans_byte = bytes([data_crc[i] ^ 0x20])
                final_data = final_data + b'\x7D' + trans_byte
            else:
                final_data = final_data + bytes([data_crc[i]])
        final_data = b'\x7E' + final_data + b'\x7E'

        self.ser.write(final_data)
        print('Enviando: ', final_data)

    def recebe(self):
        recv_data = self.ser.read()
        if(recv_data == bytearray()):
            return False
        if(self.handle_dado(recv_data, self.estado) == True):
            fcs = crc.CRC16('')
            fcs.clear()
            fcs.update(self.buffer)
            if(fcs.check_crc() == True):
                self.buffer = self.buffer[0:-2]
                return True
            if(fcs.check_crc() == False):
                print("Erro no CRC!")
                return False

    def handle(self):
        if self.recebe() == True:
            self.upper.recebe(bytes(self.buffer))
            self.buffer.clear()   

    def handle_dado(self, byte, estado):
        if(self.estado == self.Estados.ocioso):
            if(byte == b'\x7E'):
                self.n_bytes = 0
                self.estado = self.Estados.init
        if(self.estado == self.Estados.init):
            if(byte == b'\x7E'):
                self.buffer.clear()   
                return False
            if(byte == b'\x7D'):
                self.estado = self.Estados.esc
                return False
            else:
                self.buffer += byte
                self.estado = self.Estados.rx
                self.n_bytes += 1
                return False
        if(self.estado == self.Estados.rx):
            if(byte == b'\x7E'):
                self.estado = self.Estados.ocioso
                return True
            if(byte == b'\x7D'):
                self.estado = self.Estados.esc
                return False
            else:
                self.buffer += byte
                self.n_bytes += 1
                return False
        if(self.estado == self.Estados.esc):
            if(byte == b'\x7E'):
                self.buffer = bytearray()
                self.estado = self.Estados.ocioso
            else:
                byte = byte[0] ^ 0x20
                self.buffer += bytes([byte])
                self.estado = self.Estados.rx
            return False

    def handle_timeout(self):
        print('ENQ: Timeout')