from functools import reduce
from lexee.symbol import Symbol

class Variable(Symbol, dict):
    def __init__(self, name):
        super(Variable, self).__init__(name)
    
    def load(self, ctx):
        value = reduce(lambda context,item: context.get(item, getattr(self, "default")) if type(context) is dict else context , [name for name in self.identity], ctx["params"])
        setattr(self, "value", value)
        return self