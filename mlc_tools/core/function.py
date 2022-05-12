import sys
from .modifiers import Modifiers
from .object import Object, AccessSpecifier


class Function(object):

    def __init__(self):
        self.operations = []
        self.return_type = Object()
        self.name = ''
        self.args = []
        self.template_types = []
        self.is_const = False
        self.is_external = False
        self.is_static = False
        self.is_abstract = False
        self.is_template = False
        self.is_virtual = False
        self.is_friend = False
        self.is_generate = False
        self.side = 'both'
        self.access = AccessSpecifier.public
        self.body = ''
        self.translated = False
        self.specific_implementations = ''

    def get_return_type(self):
        return self.return_type

    def parse_method_body(self, body):
        operation_start_pos = 0
        curly_braces = 0
        square_brackets = 0

        for pos, char in enumerate(body):
            if char == '{':
                curly_braces += 1
            elif char == '}':
                curly_braces -= 1
            elif char in '([':
                square_brackets += 1
            elif char in ')]':
                square_brackets -= 1

            if curly_braces < 0 or square_brackets < 0:
                # TODO: Use Log.error
                print('error parsing function "{}" body'.format(self.name))
                sys.exit(-1)
            if not curly_braces and not square_brackets and char in ';}':
                operation = body[operation_start_pos:pos+1].strip()
                if operation:
                    self.operations.append(operation)
                operation_start_pos = pos + 1
                continue

        operation = body[operation_start_pos:].strip()
        if operation:
            self.operations.append(operation)

    def find_modifiers(self, string):
        if Modifiers.server in string:
            self.side = Modifiers.side_server
        if Modifiers.client in string:
            self.side = Modifiers.side_client
        self.is_external = self.is_external or Modifiers.external in string
        self.is_abstract = self.is_abstract or Modifiers.abstract in string
        self.is_static = self.is_static or Modifiers.static in string
        self.is_const = self.is_const or Modifiers.const in string
        self.is_virtual = self.is_virtual or Modifiers.virtual in string
        self.is_generate = self.is_virtual or Modifiers.generate in string

        string = AccessSpecifier.find_access(self, string)

        string = string.replace(Modifiers.server, '')
        string = string.replace(Modifiers.client, '')
        string = string.replace(Modifiers.external, '')
        string = string.replace(Modifiers.static, '')
        string = string.replace(Modifiers.const, '')
        string = string.replace(Modifiers.abstract, '')
        string = string.replace(Modifiers.virtual, '')
        string = string.replace(Modifiers.generate, '')
        return string
