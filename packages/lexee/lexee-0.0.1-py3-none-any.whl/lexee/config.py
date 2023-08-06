from lexee.symbol import Symbol

class Config(Symbol, dict):
    def __init__(self, name):
        super(Config, self).__init__(name)
    
    def load(self, ctx):
        return self