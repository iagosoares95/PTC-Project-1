#!/usr/bin/python3

import framing
from enum import Enum

class Arq:
    def __init__(self, framing):
        self.fra = framing
        self.States = Enum('')