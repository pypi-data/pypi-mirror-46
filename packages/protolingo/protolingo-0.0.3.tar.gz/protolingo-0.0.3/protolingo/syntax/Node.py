import yaml
import pykka
import inspect
import traceback
from abc import ABC, abstractmethod

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


class Node():

    def __init__(self, id, depends_on, output, exit, exitCode):
        super(Node, self).__init__()
        self.id = id
        if(output):
            self.output = output
        else:
            self.output = [id]
        self.exit = exit
        self.exitCode = exitCode
        self.depends_on = depends_on
          
    @abstractmethod
    def exec(self, **kwargs):
        pass

    def isrunnable(self):
        return len(self.output) == 1
    
    def reset(self):
        if(getattr(self,"output", None)):
            self.output = [self.id]
            self.exit = None
            self.exitCode = None
