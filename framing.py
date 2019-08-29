#!/usr/bin/python3

import serial

class Framing:

    def __init__(self, serial):
        self.States = Enum('States', 'idle rx esc')
        self.state = self.States.idle
        self.buffer = bytearray()
        self.serial = serial

    def send(self, data):
        final_data = bytearray()

        for i in range(0, len(data)):
            if((data[i] == 0x7E) or (data[i] == 0x7E)):
                trans_byte = bytearray()                
                trans_byte = data[i] ^ 0x20
                final_data = final_data + trans_byte
            else:
                final_data = final_data + bytes([data[i]])
        final_data = b'\x7E' + data + b'\x7E'
        self.seria.write(final_data)

    def receive(self):
        while(True):
            recv_data = self.serial.read()
            if(recv_data == bytearray()):
                return 0
            if(handle(byte)=True):

    def handle(self, byte):
        if(self.state == self.States.idle):
            self.state = self.idle_func(byte)
            return False
        elif(self.state == self.States.rx):
            self.state = self.rx_func(byte)
            if(self.state == self.States.idle)
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
        if(byte == b'\x7E'):
            return self.States
        elif(byte == b'\x7D')
            return self.States.esc
        elif(byte != b'\x7D' and byte != b'\x7E')
            self.buffer = self.buffer + byte
            return self.States.rx

    def esc_func(self, byte):
        trans_byte = byte ^ 0x20
        self.buffer = self.buffer + trans_byte
        return self.States.rx