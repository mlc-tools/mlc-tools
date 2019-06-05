from enum import Enum
from .modifiers import Modifiers


class AccessSpecifier(Enum):
    public = 0
    protected = 1
    private = 2

    @staticmethod
    def find_access(object_or_fucntion, string):
        if Modifiers.private in string:
            object_or_fucntion.access = AccessSpecifier.private
            string = string.replace(Modifiers.private, '')
        elif Modifiers.protected in string:
            object_or_fucntion.access = AccessSpecifier.protected
            string = string.replace(Modifiers.protected, '')
        elif Modifiers.public in string:
            object_or_fucntion.access = AccessSpecifier.public
            string = string.replace(Modifiers.public, '')
        return string

    @staticmethod
    def to_string(access):
        return {
            AccessSpecifier.public: 'public',
            AccessSpecifier.protected: 'protected',
            AccessSpecifier.private: 'private',
        }[access]


class Object(object):

    def __init__(self, type_=''):
        self.type = type_
        self.template_args = []
        self.callable_args = None
        self.name = ''
        self.initial_value = None
        self.is_pointer = False
        self.is_ref = False
        self.is_runtime = False
        self.is_static = False
        self.is_const = False
        self.is_key = False
        self.is_link = ''
        self.side = 'both'
        self.access = AccessSpecifier.public
        self.denied_intrusive = False

    def parse_type(self):
        left = self.type.find('<')
        right = -1
        try:
            right = self.type.rindex('>', left) if left != -1 else -1
        except ValueError:
            # TODO: remove exception
            exit(1)
        if left > -1 and right > -1:
            args = self.type[left + 1:right].split(',')
            self.type = self.type[0:left]
            for arg in args:
                arg = arg.strip()
                self.template_args.append(arg)
        self.is_pointer = self.check_pointer()

    def check_pointer(self):
        result = '*' in self.type
        self.type = self.type.replace('*', '')
        return result or self.is_pointer

    def check_ref(self):
        result = '&' in self.type
        self.type = self.type.replace('&', '')
        return result or self.is_ref

    def find_modifiers(self, string):
        args = ''
        left = string.find('<')
        right = string.rfind('>')
        if left != -1 and right != -1:
            args = string[left:right + 1]
            string = string[0:left] + string[right + 1:]

        if Modifiers.server in string:
            self.side = Modifiers.side_server
        if Modifiers.client in string:
            self.side = Modifiers.side_client
        self.is_runtime = self.is_runtime or Modifiers.runtime in string
        self.is_static = self.is_static or Modifiers.static in string
        self.is_key = self.is_key or Modifiers.key in string
        self.is_link = self.is_link or Modifiers.link in string
        self.is_const = self.is_const or Modifiers.const in string
        self.is_const = self.is_const or self.is_link
        self.is_pointer = self.is_pointer or Modifiers.pointer in string
        self.is_ref = self.is_ref or Modifiers.ref in string
        if self.is_link:
            self.is_pointer = True

        string = AccessSpecifier.find_access(self, string)

        string = string.replace(Modifiers.server, '')
        string = string.replace(Modifiers.client, '')
        string = string.replace(Modifiers.runtime, '')
        string = string.replace(Modifiers.const, '')
        string = string.replace(Modifiers.static, '')
        string = string.replace(Modifiers.key, '')
        string = string.replace(Modifiers.link, '')
        string = string.replace(Modifiers.ref, '')
        string = string.replace(Modifiers.pointer, '')

        if args:
            string = string[0:left] + args + string[left:]

        return string

    def set_default_initial_value(self):
        # TODO: move to Translator
        # convert initial value
        if self.initial_value is None:
            if self.type == 'int':
                self.initial_value = "0"
            elif self.type == 'float':
                self.initial_value = "0.0"
            elif self.type == 'bool':
                self.initial_value = "false"
            elif self.type == 'string':
                self.initial_value = '""'
            elif self.is_pointer:
                self.initial_value = "nullptr"


class Objects(object):
    VOID = Object('void')
    BOOL = Object('bool')
    INT = Object('int')
    STRING = Object('string')
    FLOAT = Object('float')
