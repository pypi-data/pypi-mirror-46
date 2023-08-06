from lexee.symbol import Symbol

class Import(Symbol, dict):
    def __init__(self, name):
        super(Import, self).__init__(name)
    
    def load(self, ctx):
        self.module = __import__(self.module)
        return self
    
    def resolve(self, name):
        return getattr(self.module, name)