
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
import yaml
import pykka
import inspect
import importlib
import protolingo.vernacular as language
from jinja2 import Environment, BaseLoader
from protolingo.syntax.Graph import Graph
from protolingo.utils import load_classes, load_all_modules_from_dir

def traverse_yaml_nodes(node):
    if isinstance(node, yaml.ScalarNode):
        return node.value
    elif isinstance(node, yaml.SequenceNode):
        return [traverse_yaml_nodes(item) for item in node.value]
    elif isinstance(node, yaml.MappingNode):
        values = dict()
        for item_key, item_value in node.value:
            values[item_key.value] = traverse_yaml_nodes(item_value)
        return values
    return node

def default_constructor(loader, tag_suffix, node): 
    #values = traverse_yaml_nodes(node)
    classname = tag_suffix.lstrip('!').rstrip(':')
    modules = load_all_modules_from_dir(os.path.dirname(language.__file__))
    classes = load_classes(modules)
    if(classname.capitalize() in classes.keys()):
        tag = classes[classname.capitalize()]
    else:
        module_name = "dialects." + classname
        module = importlib.import_module(module_name,".")
        tag = getattr(module, classname.capitalize())
    return tag.from_yaml(loader, node)

class Parser:

    @staticmethod
    def load(file):
        yaml.add_multi_constructor('', default_constructor, Loader=yaml.SafeLoader)
        doc = yaml.safe_load(file)
        return doc

    @staticmethod
    def save(path, doc):
        with open(path, 'w', encoding = "utf-8") as yaml_file:
            output = yaml.dump(doc, default_flow_style=False)
            yaml_file.write(output)

    @staticmethod
    def parse(key, **kwargs):
        if(type(key)==list):
            return [Parser.parse(item, **kwargs) for item in Graph.parse(key)]
        if(isinstance(key, str)):
            return Parser.parse_parameters(key, **kwargs)
        return key
          
    @staticmethod
    def parse_parameters(text, **data):
        template = Environment(loader=BaseLoader).from_string(text)
        return template.render(data)
    
    @staticmethod
    def comprehend(tag, **message):
        proxy = getattr(tag,'proxy', None)
        Parser.resolve_ref(tag, **message)
        proxy = message["yaml"][tag.id]
        output = proxy.actor_ref.ask(message,)
        proxy_fields = [(field,value) for (field,value) in [(field,getattr(proxy, field)) for field in [field for field in tag.__dict__] if field !=  "proxy"]]
        for item in proxy_fields:
           setattr(tag, item[0], item[1].get())
        setattr(tag,"output", getattr(proxy, "output").get())
        setattr(tag,"exit", getattr(proxy, "exit").get())
        setattr(tag,"exitCode", getattr(proxy, "exitCode").get())
        return output
           
    @staticmethod
    def resolve_ref(tag, **message):
        proxy = getattr(tag,'proxy', None)
        if(not proxy):
            if isinstance(tag, pykka.ThreadingActor):
                if tag.id in message["yaml"].keys() :
                    raise KeyError("duplicate key '{0}' found".format(tag.id))
                args =   inspect.getfullargspec(tag.__init__).args
                params = Parser.parse([tag.__dict__.get(arg, None)for arg in args if arg != 'self'], **message)
                actor_ref = tag.start(*params, **message)
                proxy = actor_ref.proxy()
                message["yaml"][tag.id] = proxy
                setattr(tag,"proxy", proxy)

    @staticmethod
    def resolve_ref_all(tags, **message):
           for tag in tags:
               Parser.resolve_ref(tag, **message) 


    @staticmethod
    def clear(doc):
        for expression in Parser.visit(doc):
            proxy = getattr(expression, "proxy", None)
            if(proxy):
                proxy.stop()  
                delattr(expression, "proxy")
        
    @staticmethod
    def visit(node):
        try:
            if(type(node)==list):
                for item in node:
                   yield from Parser.visit(item)
            elif isinstance(node, pykka.ThreadingActor):
                fields = [getattr(node, field) for field in [field for field in node.__dict__]]
                for field in fields:
                    yield from Parser.visit(field)
                yield node

        except Exception as e:
            print(e.__str__())
