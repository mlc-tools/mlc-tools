import re
from Object import *
from Function import Function
import constants
from constants import Modifier


class Class(Object):

    def __init__(self):
        Object.__init__(self)
        self.behaviors = []
        self.members = []
        self.functions = []
        self.is_abstract = False
        self.is_serialized = False
        self.is_visitor = False
        self.is_storage = False
        self.generate_set_function = False
        self.type = 'class'
        self.group = ''
        self.side = 'both'
        self._linked = False

    def parse(self, line):
        line = line.strip()
        if self.type in line:
            line = line[len(self.type):]
        line = self.find_modifiers(line)
        type_ = self.type
        self.type = ''
        Object.parse(self, line)
        self.name = self.type
        self.type = type_
        self.behaviors = self.template_args
        self.template_args = []
        if '/' in self.name:
            k = self.name.rindex('/')
            self.group = self.name[0:k]
            self.name = self.name[k + 1:]

    def parse_body(self, parser, body):
        parser.parse(body)
        if len(parser.classes) > 0:
            print 'Not supported inbody classes'
        self.members = parser.objects
        self.functions = parser.functions
        return

    def on_linked(self, parser):
        if self._linked:
            return

        if self.generate_set_function:
            self._generate_setters_function(parser)
            self._generate_getters_function(parser)
        if not self.is_abstract:
            for function in self.functions:
                if function.is_abstract:
                    self.is_abstract = True
                    break
            for parent in self.behaviors:
                parent.on_linked(parser)

        self._linked = True

    def find_modifiers(self, string):
        self.is_abstract = self.is_abstract or Modifier.abstract in string
        self.is_serialized = self.is_serialized or Modifier.serialized in string
        self.is_visitor = self.is_visitor or Modifier.visitor in string
        self.is_storage = self.is_storage or Modifier.storage in string
        self.generate_set_function = self.generate_set_function or Modifier.set_function in string
        if Modifier.server in string:
            self.side = Modifier.side_server
        if Modifier.client in string:
            self.side = Modifier.side_client

        string = re.sub(Modifier.server, '', string)
        string = re.sub(Modifier.client, '', string)
        string = re.sub(Modifier.abstract, '', string)
        string = re.sub(Modifier.serialized, '', string)
        string = re.sub(Modifier.visitor, '', string)
        string = re.sub(Modifier.storage, '', string)
        string = re.sub(Modifier.set_function, '', string)
        return string

    def _generate_setters_function(self, parser):
        function = Function()
        function.name = constants.CLASS_FUNCTION_SET_PROPERTY
        function.return_type = 'void'
        function.args.append(['name', 'string'])
        function.args.append(['value', 'string'])

        add_function = False
        for member in self.members:
            if member.is_pointer:
                continue
            if member.is_runtime:
                continue
            if member.is_static:
                continue
            if member.is_const:
                continue
            supported_types = {'string': 'std::string', 'int': 0, 'float': 0, 'bool': 0}
            if member.type in supported_types:
                type_ = member.type
                type_ = type_ if supported_types[type_] == 0 else supported_types[type_]
                op = 'if(name == "{0}") \n{2}\nthis->{0} = strTo<{1}>(value);\n{3}'
                if len(function.operations):
                    op = 'else ' + op
                function.operations.append(op.format(member.name, type_, '{', '}'))
                add_function = True

        override = False
        if self.behaviors:
            for class_ in self.behaviors:
                if class_.is_abstract:
                    continue
                for func in class_.functions:
                    equal = func.name == function.name and func.get_return_type().type == function.get_return_type().type
                    for i, arg in enumerate(func.args):
                        equal = equal and func.args[i][1] == function.args[i][1]
                    if equal:
                        override = True
                        if len(function.operations):
                            op = 'else \n{1}\n{0}::{3}(name, value);\n{2}'
                        else:
                            op = '{0}::{3}(name, value);'
                        function.operations.append(
                            op.format(class_.name, '{', '}', constants.CLASS_FUNCTION_SET_PROPERTY))
                        break

        if add_function or not override:
            self.functions.append(function)

    def _generate_getters_function(self, parser):
        function = Function()
        function.name = constants.CLASS_FUNCTION_GET_PROPERTY
        function.return_type = 'string'
        function.args.append(['name', 'string'])
        function.is_const = True

        add_function = False

        for member in self.members:
            if member.is_pointer:
                continue
            if member.is_runtime:
                continue
            if member.is_static:
                continue
            if member.is_const:
                continue
            supported_types = ['string', 'int', 'float', 'bool']

            def get_getter(object, name_argument):
                class_ = parser.find_class(member.type)
                getter = ''
                if member.type in supported_types:
                    type_ = member.type
                    getter = 'if({4} == "{0}")\n{2}\nreturn toStr(this->{0});\n{3}'
                    getter = getter.format(member.name, type_, '{', '}', name_argument)
                elif class_ and class_.generate_set_function and (class_.side == parser.side or class_.side == 'both'):
                    getter = 'if({2}.find("{0}/") == 0)\n__begin__\nreturn {0}{1}get_property({2}.substr(strlen("{0}/")));\n__end__'
                    operator = '->' if member.is_pointer else '.'
                    getter = getter.format(member.name, operator, name_argument)
                return getter
            if member.type != 'map':
                getter = get_getter(member, 'name')
                if getter:
                    add_function = True
                    function.operations.append(getter)

        parent_class = ''
        if self.behaviors:
            for class_ in self.behaviors:
                if class_.is_abstract:
                    continue
                for func in class_.functions:
                    equal = func.name == function.name and func.get_return_type().type == function.get_return_type().type
                    for i, arg in enumerate(func.args):
                        equal = equal and func.args[i][1] == function.args[i][1]
                    if equal:
                        parent_class = class_.name
                        break

        if not parent_class:
            op = 'return "";'
        elif function.operations:
            op = 'else \n{1}\n return {0}::{3}(name);\n{2}'.\
                format(parent_class, '{', '}', constants.CLASS_FUNCTION_GET_PROPERTY)
        else:
            op = 'return {0}::{1}(name, value);'.format(parent_class, constants.CLASS_FUNCTION_GET_PROPERTY)
        function.operations.append(op)

        if add_function or not parent_class:
            self.functions.append(function)

    def add_get_type_function(self):
        if not self.is_abstract:
            member = Object()
            member.is_static = True
            member.is_const = True
            member.type = 'string'
            member.name = 'TYPE'
            member.initial_value = '"{}"'.format(self.name)
            member.access = AccessSpecifier.public
            self.members.append(member)

        function = Function()
        function.name = constants.CLASS_FUNCTION_GET_TYPE
        function.return_type = 'string'
        function.is_const = True
        function.operations.append('return {}::TYPE;'.format(self.name))
        function.link()
        self.functions.append(function)
