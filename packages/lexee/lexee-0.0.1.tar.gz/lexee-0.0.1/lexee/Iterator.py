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

class Iterator(dict):

    def __init__(self, prefix, key, source):
        self.key = key
        self.prefix = prefix
        self.source = source
    

    def __getattr__(self, name):
        prefix = "%s.%s" % (self.prefix, name)
        keys = [key for key in self.source[self.key].keys() if key.startswith(prefix)]
        if(keys):
            return Iterator(prefix, self.key, self.source)
        else:
            value = getattr(self.source[self.key].get(self.prefix), name, None)
            if(value):
                return value.get()
