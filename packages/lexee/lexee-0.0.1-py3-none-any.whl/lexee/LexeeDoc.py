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
 
import sys
from antlr4 import *
from functools import reduce
from pylingo.pyVisitor import pyVisitor
from pylingo.pylingoLexer import pylingoLexer
from pylingo.pylingoParser import pylingoParser
from protolingo.yaml.Parser import Parser
from lexee.interpreter import Interpreter
from protolingo.utils import gettype
from lexee.symbols.data import Data
from lexee.symbols.config import Config
from lexee.symbols.variable import Variable
from lexee.symbols.generator import Generator
from lexee.Iterator import Iterator

class LexeeDoc:

    def __init__(self, symbols, params):
        self.context =  {**params, "yaml":{}}
        self.config = reduce(lambda default,item:item, [symbol.load(**self.context) for symbol in symbols if type(symbol) is Config ], dict())
        self.context["config"] = self.config
        self.context["import"] = { symbol.identity[0] : symbol.load(**self.context)  for symbol in  [symbol for symbol in symbols if symbol.name == "import" ] }
        self.context["data"] = Iterator("data", "yaml", self.context)
        self.context["variable"] = Iterator("variable", "yaml", self.context)
        self.context["generator"] = Iterator("generator", "yaml", self.context)
        self.doc = [symbol.load(**self.context) for symbol in symbols if type(symbol) in [Variable,Generator,Data]]
        
       
    def __iter__(self):
       for expression in Parser.parse(self.doc, **self.context):
           output =  Parser.comprehend(expression, **self.context) 
           yield output
           exception = gettype(output[3])
           if(((exception is SystemExit and int(output[4]) != 0) or (exception is not SystemExit)) and getattr(self.config, "exit_on_error", "True") == "True"):
                break

    def save(self, path):
        self.close()
        Parser.save(path, self.doc)

    def close(self):
        Parser.clear(self.doc)
          
    @staticmethod
    def open(path, params):
        input_stream = FileStream(path)
        lexer = pylingoLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = pylingoParser(stream)
        tree = parser.lexee()
        if(parser.getNumberOfSyntaxErrors()):
            sys.exit(-1)

        interpreter = Interpreter()
        interpreter.visit(tree)
        return LexeeDoc(interpreter.symbols, params)
