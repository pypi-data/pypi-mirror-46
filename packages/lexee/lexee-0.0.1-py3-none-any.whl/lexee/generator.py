from functools import reduce
from lexee.symbol import Symbol


class Generator(Symbol, dict):
    def __init__(self, name):
        super(Generator, self).__init__(name)
    
    def load(self, ctx):
        print('OK')