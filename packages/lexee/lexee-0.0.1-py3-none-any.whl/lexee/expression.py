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
 
import yaml 
from protolingo.yaml.Parser import Parser
from protolingo.yaml.YAMLExpression import YAMLExpression

class LexeeExpressionType(yaml.YAMLObjectMetaclass):
    def __new__(mcls, name, bases, attrs):
        if("yaml_tag" not in attrs.keys()):
            newattrs = { "yaml_tag": u"!%s" % name.lower() }
            for attrname, attrvalue in attrs.items():
                newattrs[attrname] = attrvalue
            attrs = newattrs
        return super(LexeeExpressionType, mcls).__new__(mcls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        if("yaml_tag" not in attrs.keys()):
            newattrs = { "yaml_tag": u"!%s" % name.lower() }
            for attrname, attrvalue in attrs.items():
                newattrs[attrname] = attrvalue
            attrs = newattrs
        return super(LexeeExpressionType, self).__init__(name, bases, attrs)
    


class LexeeExpression(YAMLExpression, metaclass=LexeeExpressionType):

    def __init__(self, id=None, depends_on=None, output=None, exit=None, exitCode=None, symbol=None, **kwargs):
        if(id is not None):
            super(YAMLExpression, self).__init__(id, depends_on, output, exit, exitCode)
        else:
            super(yaml.YAMLObject, self).__init__()   
        symbol.bind(self, **kwargs)
        


    def __repr__(self):
        return "%s(id=%r)" % (
            self.__class__.__name__, self.id)


