 #  Copyright 2019  Dialect Software LLC or its affiliates. All Rights Reserved.
 #
 #  Licensed under the MIT License (the "License").
 #
 #  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 #  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 #  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 #  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 #  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 #  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 #  SOFTWARE.
 
from functools import reduce
from lexee.interfaces import IInterface
from protolingo.yaml.Parser import Parser
from protolingo.yaml.YAMLExpression import YAMLExpression

class Symbol(IInterface, dict):

    def __init__(self, name:str):
        super(Symbol, self).__init__()
        self.name = name
        self.identity = []
        self.current = []
        self.depends_on = []

    def __str__(self):
        return self.name


    def bind(self, expression:YAMLExpression, **kwargs):  
        bind = True if getattr(expression,"id", None) else False
        output = [setattr(expression,key,self.bind_parameters(value, **kwargs) if bind else value) if key != "identity" else setattr(expression,"id", "%s.%s" % (self.name , ".".join(value))) if getattr(expression,"id", None) is None else True for (key,value) in self.__dict__.items() if key not in ["name","current","description"]]
        is_proxy_instance = reduce(lambda context,item : True if item or context else False, output, None)
        expression.symbol = self  
        return expression

    def bind_parameters(self, value, **kwargs):
        __dict__ = getattr(value,"__dict__", None)
        if(__dict__):
           for name in __dict__.keys():
              __dict__[name] = bind_parameters(__dict__.get(name), **kwargs)
           return __dict__
        else:
            return Parser.parse(value, **kwargs)

    __repr__ = __str__