
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

 
from .Parser import Parser
from functools import reduce
from protolingo.utils import gettype


class YAMLDoc:

    def __init__(self, path, params):
        self.context = {**params, "yaml":{}}
        with open(path, 'r') as file:
            self.doc = Parser.load(file)
        self.config = reduce(lambda default,item:item, [tag["config"] for tag in self.doc if type(tag) is dict and list(tag)[0] == "config"],dict())
        self.context["config"] = self.config
       
    def __iter__(self):
       for expression in Parser.parse(self.doc):
            output =  Parser.comprehend(expression, **self.context) 
            yield output
            exception = gettype(output[3])
            if(((exception is SystemExit and int(output[4]) != 0) or (exception is not SystemExit)) and self.config.get("exit_on_error",True)):
                break

    def save(self, path):
        self.close()
        Parser.save(path, self.doc)

    def close(self):
        Parser.clear(self.doc)
          
    @staticmethod
    def open(path, params):
        doc = Parser.load(path)
        return YAMLDoc(doc, params)

      
        