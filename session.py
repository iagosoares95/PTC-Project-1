# -*- coding: utf-8 -*-

import arq
import enlace
from enum import Enum

class Sessao:

    def __init__(elf,arq,timeout):
        states=Enum('states', 'disc hand1 hand2 con check half1 half2')
        self.States=states

