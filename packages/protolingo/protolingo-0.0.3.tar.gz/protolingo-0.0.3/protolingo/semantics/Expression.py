
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
import pykka
import inspect
from protolingo.utils import capture, marshal_output
from protolingo.syntax.Node import Node


class Expression(Node, pykka.ThreadingActor):

    def __init__(self, id, depends_on=[], output=None, exit=None, exitCode = None):
        super(Expression, self).__init__(id, depends_on, output, exit, exitCode)
       
    def on_failure(self, exception_type, exception_value, traceback):
         super(Expression, self).on_failure(exception_type, exception_value, traceback)

    def on_stop(self):
        super(Expression, self).on_stop()

    def on_receive(self, message):
        # NEEDS TO BE CONSISTENT WITH MARSHAL
        try:
            if(self.isrunnable()):
                with capture() as out:
                    self.exec(**message)
                self.output += out
                self.exit = out[2]
                self.exitCode =  None
                if(len(out) > 4):
                    self.exitCode = out[3]
            return self.output
        except:
            raise

    def reset(self):
        proxy = getattr(self, "proxy", None)
        if proxy:
            proxy.reset()
        else:
            super(Expression, self).reset()
