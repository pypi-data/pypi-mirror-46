from abc import ABC
from units import BaseUnit
from interface import *


class Army(ABC):
    def __init__(self):
        self.units = Composite()
        self.cnt = 0

    def action(self):
        pass        
    
    def add_unit(self, unit: BaseUnit):
        self.cnt += 1
        self.units.add(unit)