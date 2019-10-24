#!/usr/bin/python3

import serial
import crc
from enum import Enum
from binascii import unhexlify
import time

class Framing:

    def __init__(self, serial, timeout):
        self.States = Enum('States', 'idle rx esc')
        self.state = self.States.idle
        self.buffer = bytearray()
        self.ser = serial
        self.timeout = timeout
        self.l_time = time.time()
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def send(self, data):
        final_data = bytearray()
        fcs = crc.CRC16(data)
        data_crc = fcs.gen_crc()
        #print('crc:',data_crc)

        for i in range(0, len(data_crc)):
            if((data_crc[i] == 0x7E) or (data_crc[i] == 0x7E)):
                trans_byte = bytes([data_crc[i] ^ 0x20])
                final_data = final_data + b'\x7D' + trans_byte
            else:
                final_data = final_data + bytes([data_crc[i]])
        final_data = b'\x7E' + final_data + b'\x7E'
        self.ser.write(final_data)
        print('Sending: ', final_data)

    def receive(self):
        while(True):
            recv_data = self.ser.read()
            if(recv_data == bytearray()):
                return bytearray()
            if(self.handle(recv_data) == True):
                buf = self.buffer
                fcs = crc.CRC16('')
                fcs.clear()
                fcs.update(self.buffer)
                if(fcs.check_crc() == True):
                    print('Recebido:',buf[0:-2])
                    return buf[0:-2]
                else:
                    buf = bytearray()
                    return buf

    def handle(self, byte):
        if(self.state == self.States.idle):
            self.state = self.idle_func(byte)
            return False
        elif(self.state == self.States.rx):
            self.state = self.rx_func(byte)
            if(self.state == self.States.idle):
                return True
            return False
        elif(self.state == self.States.esc):
            self.state = self.esc_func(byte)
            return False
        
    def idle_func(self, byte):
        if(byte == b'\x7E'):
            self.buffer = bytearray()
            return self.States.rx
        else:
            return self.States.idle
            
    def rx_func(self, byte):
        self.l_time = time.time()
        if(byte == b'\x7E'):
            return self.States.idle
        elif(byte == b'\x7D'):
            return self.States.esc
        elif(byte != b'\x7D' and byte != b'\x7E'):
            self.buffer = self.buffer + byte
            return self.States.rx

    def esc_func(self, byte):
        self.l_time = time.time()
        trans_byte = byte[0] ^ 0x20
        self.buffer = self.buffer + bytes([trans_byte])
        return self.States.rx

    def timeout_func(self):
        if(self.state in [self.States.rx, self.States.esc]):
            diff_time = time.time() - self.l_time
            if(diff_time > self.timeout):
                print("Timeout framing")
                self.buffer = bytearray()
                self.state = self.States.idle