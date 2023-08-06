from functools import reduce
from lexee.symbol import Symbol

class Data(Symbol, dict):
    def __init__(self, name):
        super(Data, self).__init__(name)
    
    def load(self, ctx):
        print('OK')