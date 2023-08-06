
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
 


import re
import sys
import inspect
import pkgutil
import contextlib
import traceback

import json
import codecs

_ansi_regex = r'\x1b(' \
             r'(\[\??\d+[hl])|' \
             r'([=<>a-kzNM78])|' \
             r'([\(\)][a-b0-2])|' \
             r'(\[\d{0,2}[ma-dgkjqi])|' \
             r'(\[\d+;\d+[hfy]?)|' \
             r'(\[;?[hf])|' \
             r'(#[3-68])|' \
             r'([01356]n)|' \
             r'(O[mlnp-z]?)|' \
             r'(/Z)|' \
             r'(\d+)|' \
             r'(\[\?\d;\d0c)|' \
             r'(\d;\dR))'

_ansi_escape = re.compile(_ansi_regex, flags=re.IGNORECASE)
escape = lambda text : _ansi_escape.sub('',text)


@contextlib.contextmanager
def capture():
    import sys
    from io import StringIO
    out=[StringIO(), StringIO()]
    oldout,olderr = sys.stdout, sys.stderr
    try:
        sys.stdout,sys.stderr = out
        yield out
    except:
        pass
    finally:
        sys.stdout,sys.stderr = oldout, olderr
        out[0] = codecs.encode(out[0].getvalue(), 'unicode-escape')
        out[1] = codecs.encode(out[1].getvalue(), 'unicode-escape')
        exit_info = sys.exc_info()
        if(exit_info[0]):
            out.append(sys.exc_info()[0].__name__)
            out.append(sys.exc_info()[1].__str__())
            out.append(codecs.encode(traceback.format_exc(), 'unicode-escape'))
        else:
           out.append(None)


#TODO Upgrade to 3.7 Build types.Traceback
#TODO raise exception(output[4], output[5])  or raise exception(output[4]).with_traceback(output[5])
def marshal_output(output, suppress_sys_exit_0=True):
    print(codecs.decode(output[1], 'unicode-escape'), file=sys.stdout, end = '')
    print(codecs.decode(output[2], 'unicode-escape'), file=sys.stderr, end = '')
    exception = gettype(output[3])
    if (exception is SystemExit):
        if((output[4].isnumeric() and int(output[4]) == 0 and suppress_sys_exit_0) == True):
            return
        if(output[4].isnumeric()):
            raise exception(int(output[4])).with_traceback(None)
    if (exception is None):
        if(suppress_sys_exit_0):
            return
        else:
           raise SystemExit().with_traceback(None)
    raise exception(output[4]).with_traceback(None) 


def gettype(name):
    if name is None:
        return None
    t = __builtins__[name]
    if isinstance(t, type):
        return t
    raise ValueError(name)  

def load_classes(modules):
    flatten = lambda l: [item for sublist in l for item in sublist]
    return dict((clazz[0],clazz[1]) for clazz in flatten(inspect.getmembers(obj) for obj in modules) if inspect.isclass(clazz[1]))


def load_all_modules_from_dir(dirname):
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = '%s.%s' % (dirname, package_name)
        if full_package_name not in sys.modules:
            yield importer.find_module(package_name).load_module(package_name)

            
