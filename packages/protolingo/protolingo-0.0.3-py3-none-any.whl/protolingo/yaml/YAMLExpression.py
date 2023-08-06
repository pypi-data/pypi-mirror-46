
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
from protolingo.semantics.Expression import Expression

class YAMLExpression(Expression, yaml.YAMLObject):

    def __init__(self, id, depends_on=[], output=None, exit=None, exitCode = None):
        super(YAMLExpression, self).__init__(id, depends_on, output, exit, exitCode)