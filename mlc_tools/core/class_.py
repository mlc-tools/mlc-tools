import re
from .object import Object
from .modifiers import Modifiers


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
        from ..utils.common import smart_split
        line = line.strip()
        if self.type in line:
            line = line[len(self.type):]
        elif 'interface' in line:
            line = line[len('interface'):]
        line = self.find_modifiers(line)

        pattern = re.compile(r' ([\w/]+)(<(\w+)>)*')
        parts = pattern.findall(line)[0]
        self.name = parts[0]
        self.superclasses = smart_split(parts[2], ',')
        self.template_args = []
        if '/' in self.name:
            k = self.name.rindex('/')
            self.group = self.name[0:k]
            self.name = self.name[k + 1:]

    def parse_body(self, parser, body):
        parser.parse_text(body)

        for member in parser.model.objects:
            if parser.model.has_class(member.type):
                member.type = self.name + member.type
            for i, arg in enumerate(member.template_args):
                if parser.model.has_class(arg):
                    member.template_args[i] = self.name + member.template_args[i]

        for func in parser.model.functions:
            if parser.model.has_class(func.return_type):
                func.return_type = self.name + func.return_type
            for arg in func.args:
                if parser.model.has_class(arg[1]):
                    arg[1] = self.name + arg[1]

            for cls in parser.model.classes:
                pattern = re.compile(r'\b{}\b'.format(cls.name))
                new_name = self.name + cls.name
                for i, line in enumerate(func.operations):
                    func.operations[i] = re.sub(pattern, new_name, line)
        for cls in parser.model.classes:
            inner_class_name = cls.name
            cls.name = self.name + cls.name
            cls.group = self.group
            cls.side = self.side
            cls.is_test = self.is_test
            self.inner_classes.append(cls)

            for obj in parser.model.objects:
                if obj.type == inner_class_name:
                    obj.type = cls.name
                for arg in obj.template_args:
                    if arg.type == inner_class_name:
                        arg.type = cls.name

            for method in parser.model.functions:
                for _, arg in method.args:
                    if arg.type == inner_class_name:
                        arg.type = cls.name
                if method.return_type.type == inner_class_name:
                    method.return_type.type = cls.name

        self.members = parser.model.objects
        self.functions = parser.model.functions

        for member in self.members:
            member.set_default_initial_value()
        return

    def on_linked(self, model):
        if self._linked:
            return

        for func in self.functions:
            func.is_virtual = self.is_virtual or \
                func.is_virtual or \
                func.is_abstract or \
                self.has_function_in_subclasses(func)
            func.is_virtual = func.is_virtual or \
                self.has_function_in_superclasses(func)

        if not self.is_abstract:
            for method in self.functions:
                if method.is_abstract:
                    self.is_abstract = True
                    method.is_virtual = True
                    break
            for superclass in self.superclasses:
                superclass.on_linked(model)

        self._linked = True

    def has_function_in_subclasses(self, method):
        for subclass in self.subclasses:
            for func in subclass.functions:
                equal = True
                equal = equal and func.name == method.name
                # TODO: compare arguments
                # equal = equal and func.args == function.args
                equal = equal and func.return_type.type == method.return_type.type
                if equal:
                    func.is_virtual = True
                    return True
        for subclass in self.subclasses:
            if subclass.has_function_in_subclasses(method):
                return True
        return False

    def has_function_in_superclasses(self, method):
        for superclass in self.superclasses:
            for func in superclass.functions:
                equal = True
                equal = equal and func.name == method.name
                # equal = equal and func.args == function.args
                equal = equal and func.return_type.type == method.return_type.type
                if equal:
                    func.is_virtual = True
                    return True
        for superclass in self.superclasses:
            if superclass.has_function_in_superclasses(method):
                return True
        return False

    def find_modifiers(self, string):
        self.is_abstract = self.is_abstract or Modifiers.abstract in string
        self.is_serialized = self.is_serialized or Modifiers.serialized in string
        self.is_visitor = self.is_visitor or Modifiers.visitor in string
        self.is_storage = self.is_storage or Modifiers.storage in string
        self.is_numeric = self.is_numeric or Modifiers.numeric in string
        self.is_test = self.is_test or Modifiers.test in string
        self.is_inline = self.is_inline or Modifiers.inline in string
        self.is_virtual = self.is_virtual or Modifiers.virtual in string
        self.generate_set_function = self.generate_set_function or Modifiers.set_function in string
        if Modifiers.server in string:
            self.side = Modifiers.side_server
        if Modifiers.client in string:
            self.side = Modifiers.side_client

        string = string.replace(Modifiers.server, '')
        string = string.replace(Modifiers.client, '')
        string = string.replace(Modifiers.abstract, '')
        string = string.replace(Modifiers.serialized, '')
        string = string.replace(Modifiers.visitor, '')
        string = string.replace(Modifiers.storage, '')
        string = string.replace(Modifiers.set_function, '')
        string = string.replace(Modifiers.numeric, '')
        string = string.replace(Modifiers.test, '')
        string = string.replace(Modifiers.inline, '')
        string = string.replace(Modifiers.virtual, '')
        return string
