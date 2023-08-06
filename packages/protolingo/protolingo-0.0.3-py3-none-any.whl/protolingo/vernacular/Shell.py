
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
from protolingo.utils import escape
from protolingo.yaml.YAMLExpression import YAMLExpression


class Shell(YAMLExpression):
    yaml_tag = u'!shell'

    def __init__(self, id, depends_on, commands, output=None, exit=None, exitCode=None):
        super(YAMLExpression, self).__init__(id, depends_on, output, exit, exitCode)
        self.commands = commands

    def exec(self,**kwargs):
        try:
            for command in self.commands:
                print(command)
                proc = subprocess.Popen(command,
                env = {**os.environ},
                shell  = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                )
                stdout, stderr = proc.communicate()
                print(escape(stdout.decode("utf-8")), file=sys.stdout, end = '')
                print(escape(stderr.decode("utf-8")), file=sys.stderr, end = '')
                if proc.returncode != 0 :
                    break
            sys.exit(proc.returncode)
        except Exception as e:
            print(e.__str__(), file=sys.stderr)
            raise

    def __repr__(self):
        return "%s(id=%r, commands=%r)" % (
            self.__class__.__name__, self.id, self.commands)

