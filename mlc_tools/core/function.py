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
        self.side = 'both'
        self.access = AccessSpecifier.public
        self.body = ''
        self.translated = False
        self.specific_implementations = ''

    def get_return_type(self):
        return self.return_type

    def parse_body(self, body):
        counters = {}
        dividers = ['{}', '()']
        operations = []
        operation = ''

        def counters_sum():
            result = 0
            for counter in counters:
                result += counters[counter]
            return result

        for char in body:
            for div in dividers:
                if char in div:
                    if div not in counters:
                        counters[div] = 0
                    counters[div] += 1 if char == div[0] else -1
            if counters_sum() < 0:
                print('error parsing function "{}" body'.format(self.name))
                exit(-1)
            operation += char
            if counters_sum() == 0 and char in ';}':
                operations.append(operation.strip())
                operation = ''
                continue
        operations.append(operation.strip())
        self.operations = [o for o in operations if o]
        return

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

        string = AccessSpecifier.find_access(self, string)

        string = string.replace(Modifiers.server, '')
        string = string.replace(Modifiers.client, '')
        string = string.replace(Modifiers.external, '')
        string = string.replace(Modifiers.static, '')
        string = string.replace(Modifiers.const, '')
        string = string.replace(Modifiers.abstract, '')
        string = string.replace(Modifiers.virtual, '')
        return string
