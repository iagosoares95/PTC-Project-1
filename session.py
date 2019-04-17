# -*- coding: utf-8 -*-

import arq
import enlace
from enum import Enum

class Sessao:

    def __init__(elf,arq,timeout):
        self.states=Enum('states', 'disc hand1 hand2 con check half1 half2')
        self.States=self.states.disc
        self.arq=arq
        self.timeout=timeout
        self.max_no_resp=3

    def inicia(self):

