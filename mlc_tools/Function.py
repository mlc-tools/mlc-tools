import re
from .constants import Modifier
from .Object import Object, AccessSpecifier


class Function:

    def __init__(self):
        self.operations = []
        self.return_type = Object()
        self.name = ''
        self.args = []
        self.is_const = False
        self.is_external = False
        self.is_static = False
        self.is_abstract = False
        self.is_template = False
        self.is_virtual = False
        self.side = 'both'
        self.access = AccessSpecifier.public

    def parse(self, line):
        line = line.strip()
        k = line.find('function')
        if k == 0:
            line = line[k + 8:].strip()
        args_s = line[line.find('(') + 1:line.find(')')]
        args = []
        counter = 0
        k = 0
        i = 0
        for ch in args_s:
            if ch == '<':
                counter += 1
            if ch == '>':
                counter -= 1
            if counter == 0 and (ch == ',' or i == len(args_s) - 1):
                r = i if i < len(args_s) - 1 else i + 1
                args.append(args_s[k:r])
                k = i + 1
            i += 1

        if args and args[0]:
            for arg in args:
                arg = arg.strip()
                is_const = False
                if arg.startswith('const '):
                    is_const = True
                    arg = arg[len('const '):]

                def p(char, string):
                    index = -1
                    counter = 0
                    for i, c in enumerate(string):
                        if c == '<':
                            counter += 1
                        if c == '>':
                            counter -= 1
                        if counter == 0 and c == char:
                            index = i
                            break
                    if index == -1:
                        return False

                    type_ = (string[:index].strip() + char).strip()
                    if is_const:
                        type_ = 'const ' + type_
                    name = string[index + 1:].strip()
                    self.args.append([name, type_])
                    return True

                if not (p('*', arg) or p('&', arg) or p(' ', arg)):
                    print('TODO: exit - 1. Function 1')
                    print('Parsed line: [%s]' % line)
                    exit(-1)

        line = line[:line.find('(')] + line[line.rfind(')') + 1:]
        line = line.replace(';', '')
        line = re.sub(r'{.*}', '', line)
        k = line.rfind(' ')
        return_s = line[:k].strip()
        name_s = line[k:].strip()

        self.return_type = return_s
        name_s = self._find_modifiers(name_s)
        self.name = name_s
        return

    def get_return_type(self):
        if isinstance(self.return_type, str):
            self.link()
        return self.return_type

    def link(self):
        if not isinstance(self.return_type, str):
            return

        return_type = self.return_type
        self.return_type = Object()
        self.return_type.parse(return_type)

    def parse_body(self, body):
        counters = {}
        dividers = ['{}', '()']
        operations = []
        operation = ''

        def counter():
            sum = 0
            for div in counters:
                sum += counters[div]
            return sum

        for ch in body:
            for div in dividers:
                if ch in div:
                    if div not in counters:
                        counters[div] = 0
                    counters[div] += 1 if ch == div[0] else -1
            if counter() < 0:
                print('error parsing function "{}" body'.format(self.name))
                exit(-1)
            operation += ch
            if counter() == 0 and ch in ';}':
                operations.append(operation.strip())
                operation = ''
                continue
        operations.append(operation.strip())
        self.operations = [o for o in operations if o]
        return

    def _find_modifiers(self, string):
        if Modifier.server in string:
            self.side = Modifier.side_server
        if Modifier.client in string:
            self.side = Modifier.side_client
        self.is_external = self.is_external or Modifier.external in string
        self.is_abstract = self.is_abstract or Modifier.abstract in string
        self.is_static = self.is_static or Modifier.static in string
        self.is_const = self.is_const or Modifier.const in string
        self.is_virtual = self.is_virtual or Modifier.virtual in string

        if Modifier.private in string:
            self.access = AccessSpecifier.private
        if Modifier.protected in string:
            self.access = AccessSpecifier.protected
        if Modifier.public in string:
            self.access = AccessSpecifier.public

        string = string.replace(Modifier.server, '')
        string = string.replace(Modifier.client, '')
        string = string.replace(Modifier.external, '')
        string = string.replace(Modifier.static, '')
        string = string.replace(Modifier.const, '')
        string = string.replace(Modifier.abstract, '')
        string = string.replace(Modifier.private, '')
        string = string.replace(Modifier.protected, '')
        string = string.replace(Modifier.public, '')
        string = string.replace(Modifier.virtual, '')
        return string
