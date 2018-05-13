import re
from .constants import Modifier


class AccessSpecifier:
    public = 0
    protected = 1
    private = 2


class Object:

    def __init__(self):
        self.type = ''
        self.template_args = []
        self.name = ''
        self.initial_value = None
        self.is_pointer = False
        self.is_runtime = False
        self.is_static = False
        self.is_const = False
        self.is_key = False
        self.is_link = ''
        self.side = 'both'
        self.access = AccessSpecifier.public

    def parse(self, line):
        line = line.strip()
        line = self.find_modifiers(line)
        line = re.sub(';', '', line)
        line = re.sub(', ', ',', line)
        line = re.sub(' ,', ',', line)
        expression = ''
        if '=' in line:
            k = line.find('=')
            expression = line[k + 1:].strip()
            line = line[0:k].strip()
        args = line.split(' ')
        for arg in args:
            arg = arg.strip()
            if not arg:
                continue
            if not self.type:
                self.type = arg
            elif not self.name:
                self.name = arg

        if expression:
            self.initial_value = expression

        if self.access == AccessSpecifier.public:
            if self.name.startswith('__'):
                self.access = AccessSpecifier.private
            elif self.name.startswith('_'):
                self.access = AccessSpecifier.protected

        self.parse_type()

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

    def parse_type(self):
        l = self.type.find('<')
        r = self.type.rindex('>', l) if l != -1 else -1
        if l > -1 and r > -1:
            args = self.type[l + 1:r].split(',')
            self.type = self.type[0:l]
            for arg in args:
                arg = arg.strip()
                self.template_args.append(arg)
        self.is_pointer = self.check_pointer()

    def check_pointer(self):
        result = '*' in self.type
        self.type = re.sub('\*', '', self.type)
        return result

    def find_modifiers(self, string):
        args = ''
        l = string.find('<')
        r = string.rfind('>')
        if l != -1 and r != -1:
            args = string[l:r + 1]
            string = string[0:l] + string[r + 1:]

        if Modifier.server in string:
            self.side = Modifier.side_server
        if Modifier.client in string:
            self.side = Modifier.side_client
        self.is_runtime = self.is_runtime or Modifier.runtime in string
        self.is_static = self.is_static or Modifier.static in string
        self.is_key = self.is_key or Modifier.key in string
        self.is_link = self.is_link or Modifier.link in string
        self.is_const = self.is_const or Modifier.const in string
        self.is_const = self.is_const or self.is_link

        if Modifier.private in string:
            self.access = AccessSpecifier.private
        if Modifier.protected in string:
            self.access = AccessSpecifier.protected
        if Modifier.public in string:
            self.access = AccessSpecifier.public

        string = re.sub(Modifier.server, '', string)
        string = re.sub(Modifier.client, '', string)
        string = re.sub(Modifier.runtime, '', string)
        string = re.sub(Modifier.const, '', string)
        string = re.sub(Modifier.static, '', string)
        string = re.sub(Modifier.key, '', string)
        string = re.sub(Modifier.link, '', string)
        string = re.sub(Modifier.private, '', string)
        string = re.sub(Modifier.protected, '', string)
        string = re.sub(Modifier.public, '', string)

        if args:
            string = string[0:l] + args + string[l:]

        return string
