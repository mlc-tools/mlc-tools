import re
from . import constants
from .Object import *
from .Function import Function
from .constants import Modifier


class Class(Object):

    def __init__(self):
        Object.__init__(self)
        self.superclasses = []
        self.subclasses = []
        self.members = []
        self.functions = []
        self.is_abstract = False
        self.is_serialized = False
        self.is_visitor = False
        self.is_storage = False
        self.is_numeric = False
        self.is_test = False
        self.is_inline = False
        self.is_virtual = False
        self.generate_set_function = False
        self.type = 'class'
        self.group = ''
        self.side = 'both'
        self.auto_generated = True
        self.inner_classes = []
        self._linked = False

    def parse(self, line):
        line = line.strip()
        if self.type in line:
            line = line[len(self.type):]
        elif 'interface' in line:
            line = line[len('interface'):]
        line = self.find_modifiers(line)
        type_ = self.type
        self.type = ''
        Object.parse(self, line)
        self.name = self.type
        self.type = type_
        self.superclasses = self.template_args
        self.template_args = []
        if '/' in self.name:
            k = self.name.rindex('/')
            self.group = self.name[0:k]
            self.name = self.name[k + 1:]

    def parse_body(self, parser, body):
        parser.parse(body)

        for member in parser.objects:
            if parser.find_class(member.type):
                member.type = self.name + member.type
            for i, arg in enumerate(member.template_args):
                if parser.find_class(arg):
                    member.template_args[i] = self.name + member.template_args[i]

        for func in parser.functions:
            if parser.find_class(func.return_type):
                func.return_type = self.name + func.return_type
            for arg in func.args:
                if parser.find_class(arg[1]):
                    arg[1] = self.name + arg[1]

            for cls in parser.classes:
                pattern = re.compile(r'\b{}\b'.format(cls.name))
                repl = self.name + cls.name
                for i, op in enumerate(func.operations):
                    func.operations[i] = re.sub(pattern, repl, op)
        for cls in parser.classes:
            cls.name = self.name + cls.name
            cls.group = self.group
            cls.size = self.side
            cls.is_test = self.is_test
            self.inner_classes.append(cls)

        self.members = parser.objects
        self.functions = parser.functions
        return

    def on_linked(self, parser):
        if self._linked:
            return

        if self.generate_set_function:
            self._generate_setters_function(parser)
            self._generate_getters_function(parser)

        for func in self.functions:
            func.is_virtual = self.is_virtual or \
                              func.is_virtual or \
                              func.is_abstract or \
                              self._has_equal_function_in_subclasses(func)
            func.is_virtual = func.is_virtual or \
                              self._has_equal_function_in_superclasses(func)

        if not self.is_abstract:
            for function in self.functions:
                if function.is_abstract:
                    self.is_abstract = True
                    function.is_virtual = True
                    break
            for superclass in self.superclasses:
                superclass.on_linked(parser)

        self._linked = True

    def _has_equal_function_in_subclasses(self, function):
        for subclass in self.subclasses:
            for func in subclass.functions:
                equal = True
                equal = equal and func.name == function.name
                # equal = equal and func.args == function.args
                equal = equal and func.return_type.type == function.return_type.type
                if equal:
                    func.is_virtual = True
                    return True
        for subclass in self.subclasses:
            if subclass._has_equal_function_in_subclasses(function):
                return True
        return False

    def _has_equal_function_in_superclasses(self, function):
        for superclass in self.superclasses:
            for func in superclass.functions:
                equal = True
                equal = equal and func.name == function.name
                # equal = equal and func.args == function.args
                equal = equal and func.return_type.type == function.return_type.type
                if equal:
                    func.is_virtual = True
                    return True
        for superclass in self.superclasses:
            if superclass._has_equal_function_in_superclasses(function):
                return True
        return False

    def find_modifiers(self, string):
        self.is_abstract = self.is_abstract or Modifier.abstract in string
        self.is_serialized = self.is_serialized or Modifier.serialized in string
        self.is_visitor = self.is_visitor or Modifier.visitor in string
        self.is_storage = self.is_storage or Modifier.storage in string
        self.is_numeric = self.is_numeric or Modifier.numeric in string
        self.is_test = self.is_test or Modifier.test in string
        self.is_inline = self.is_inline or Modifier.inline in string
        self.is_virtual = self.is_virtual or Modifier.virtual in string
        self.generate_set_function = self.generate_set_function or Modifier.set_function in string
        if Modifier.server in string:
            self.side = Modifier.side_server
        if Modifier.client in string:
            self.side = Modifier.side_client

        string = string.replace(Modifier.server, '')
        string = string.replace(Modifier.client, '')
        string = string.replace(Modifier.abstract, '')
        string = string.replace(Modifier.serialized, '')
        string = string.replace(Modifier.visitor, '')
        string = string.replace(Modifier.storage, '')
        string = string.replace(Modifier.set_function, '')
        string = string.replace(Modifier.numeric, '')
        string = string.replace(Modifier.test, '')
        string = string.replace(Modifier.inline, '')
        string = string.replace(Modifier.virtual, '')
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
        if self.superclasses:
            for class_ in self.superclasses:
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

        superclass = ''
        if self.superclasses:
            for class_ in self.superclasses:
                if class_.is_abstract:
                    continue
                for func in class_.functions:
                    equal = func.name == function.name and func.get_return_type().type == function.get_return_type().type
                    for i, arg in enumerate(func.args):
                        equal = equal and func.args[i][1] == function.args[i][1]
                    if equal:
                        superclass = class_.name
                        break

        if not superclass:
            op = 'return "";'
        elif function.operations:
            op = 'else \n{1}\n return {0}::{3}(name);\n{2}'.\
                format(superclass, '{', '}', constants.CLASS_FUNCTION_GET_PROPERTY)
        else:
            op = 'return {0}::{1}(name, value);'.format(superclass, constants.CLASS_FUNCTION_GET_PROPERTY)
        function.operations.append(op)

        if add_function or not superclass:
            self.functions.append(function)

    def add_get_type_function(self):
        # if not self.is_abstract:
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
        # function.is_abstract = self.is_abstract
        if not function.is_abstract:
            function.operations.append('return {}::TYPE;'.format(self.name))
        function.link()
        self.functions.append(function)
        function.is_virtual = self.is_virtual or len(self.superclasses) or len(self.subclasses)
