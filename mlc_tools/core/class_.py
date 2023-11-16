import re

from .function import Function
from .object import Object
from .modifiers import Modifiers
from ..utils.error import Error


class Class(Object):

    OPERATOR_MATCH = re.compile(r'operator\b.+')

    def __init__(self, name=''):
        Object.__init__(self)
        self.superclasses = []
        self.subclasses = []
        self.constructor = None
        self.members = []
        self.functions = []
        self.user_includes = set()
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
        self.prefer_use_forward_declarations = False

        self.name = name

    def has_method_with_name(self, name):
        for method in self.functions:
            if method.name == name:
                return True
        return False

    def has_member_with_name(self, name):
        for member in self.members:
            if member.name == name:
                return True
        return False

    def get_method_with_name(self, name) -> Function or None:
        for method in self.functions:
            if method.name == name:
                return method
        return None

    def has_abstract_method(self):
        for method in self.functions:
            if method.is_abstract:
                return True
        return False

    def has_virtual_table(self):
        result = False
        result = result or self.is_virtual
        result = result or self.superclasses
        result = result or self.subclasses
        result = result or self.has_abstract_method()
        return result

    def on_linked(self, model):
        if self._linked:
            return

        for func in self.functions:
            func.is_virtual = self.is_virtual or \
                func.is_virtual or \
                func.is_abstract or \
                self.has_function_in_subclasses(func)

            # if 'operator' in func.name:
            if Class.OPERATOR_MATCH.findall(func.name):
                func.is_virtual = False
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

    @staticmethod
    def __has_function(list_of_classes, method):
        for cls in list_of_classes:
            for func in cls.functions:
                equal = True
                equal = equal and func.name == method.name
                equal = equal and func.return_type.type == method.return_type.type and 'operator' not in func.name
                if equal:
                    func.is_virtual = True
                    return True
        # for cls in list_of_classes:
        #     if cls.has_function_in_subclasses(method):
        #         return True
        return False


    def has_function_in_subclasses(self, method):
        return Class.__has_function(self.subclasses, method)

    def has_function_in_superclasses(self, method):
        return Class.__has_function(self.superclasses, method)

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
        self.prefer_use_forward_declarations = self.prefer_use_forward_declarations or Modifiers.prefer_use_forward_declarations in string

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
        string = string.replace(Modifiers.prefer_use_forward_declarations, '')

        return string

    def generate_constructor(self):
        counter = 0
        for method in self.functions:
            if method.name == 'constructor':
                self.constructor = method
                if counter > 0:
                    Error.exit(Error.CLASS_HAVE_MORE_THAN_ONE_CONSTRUCTOR, self.name)

        if self.constructor and self.constructor.is_generate:
            for member in self.members:
                arg = Object()
                arg.type = member.type
                arg.set_default_initial_value()
                self.constructor.args.append([member.name, arg])
                self.constructor.operations.append('this->{0} = {0};'.format(member.name))