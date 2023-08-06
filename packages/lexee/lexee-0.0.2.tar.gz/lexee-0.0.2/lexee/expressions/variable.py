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
 

import os
import sys
import subprocess
from functools import reduce
from protolingo.utils import escape
from lexee.symbol import Symbol
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
 
from lexee.expression import LexeeExpression
from protolingo.yaml.Parser import Parser
from protolingo.yaml.YAMLExpression import YAMLExpression


class Variable(LexeeExpression):
    
    def __init__(self, id=None, depends_on=[], output=None, exit=None, exitCode=None, symbol=None, **kwargs):
        super().__init__(id, depends_on, output, exit, exitCode, symbol, **kwargs)

    def exec(self,**kwargs):
        try:
            value = reduce(lambda context,item: context.get(item, getattr(self, "default")) if type(context) is dict else getattr(self, "default") , [name for name in self.symbol.identity], kwargs)
            setattr(self, "value", value)
            print("setting %s equal to \"%s\"..." % (self.id, value))
            sys.exit(0)
        except Exception as e:
            print(e.__str__(), file=sys.stderr)
            raise

    def __repr__(self):
        return "%s(id=%r, default=%r)" % (
            self.__class__.__name__, self.id, self.default)
