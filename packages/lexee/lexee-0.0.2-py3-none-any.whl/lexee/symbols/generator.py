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
 
import importlib
from functools import reduce
from lexee.symbol import Symbol
from lexee.Iterator import Iterator


class Generator(Symbol, dict):
    def __init__(self, name):
        super(Generator, self).__init__(name)
    
    def load(self, **kwargs):
        _import = kwargs["import"].get(self.identity[0:][0], None)
        if(_import is None):
            _import = importlib.import_module(".".join(self.identity[:-2]))
            clazz = getattr(_import,self.identity[-2:-1][0])
        else:
            clazz = _import.resolve(self.identity[1:][0])
        return clazz(symbol=self)