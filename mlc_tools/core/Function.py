import re
from .Modifiers import Modifiers
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
        self.body = ''
        self.translated = False
        self.specific_implementations = ''

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
                    counter2 = 0
                    for j, c in enumerate(string):
                        if c == '<':
                            counter2 += 1
                        if c == '>':
                            counter2 -= 1
                        if counter2 == 0 and c == char:
                            index = j
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
        if isinstance(self.return_type, str):
            return_type = self.return_type
            self.return_type = Object()
            self.return_type.parse(return_type)

        for i, arg in enumerate(self.args):
            if isinstance(arg[1], Object):
                continue
            obj = Object()
            obj.parse(arg[1])
            obj.name = arg[0]
            self.args[i][1] = obj

    def parse_body(self, body):
        counters = {}
        dividers = ['{}', '()']
        operations = []
        operation = ''

        def counters_sum():
            s = 0
            for d in counters:
                s += counters[d]
            return s

        for ch in body:
            for div in dividers:
                if ch in div:
                    if div not in counters:
                        counters[div] = 0
                    counters[div] += 1 if ch == div[0] else -1
            if counters_sum() < 0:
                print('error parsing function "{}" body'.format(self.name))
                exit(-1)
            operation += ch
            if counters_sum() == 0 and ch in ';}':
                operations.append(operation.strip())
                operation = ''
                continue
        operations.append(operation.strip())
        self.operations = [o for o in operations if o]
        return

    def _find_modifiers(self, string):
        if Modifiers.server in string:
            self.side = Modifiers.side_server
        if Modifiers.client in string:
            self.side = Modifiers.side_client
        self.is_external = self.is_external or Modifiers.external in string
        self.is_abstract = self.is_abstract or Modifiers.abstract in string
        self.is_static = self.is_static or Modifiers.static in string
        self.is_const = self.is_const or Modifiers.const in string
        self.is_virtual = self.is_virtual or Modifiers.virtual in string

        if Modifiers.private in string:
            self.access = AccessSpecifier.private
        if Modifiers.protected in string:
            self.access = AccessSpecifier.protected
        if Modifiers.public in string:
            self.access = AccessSpecifier.public

        string = string.replace(Modifiers.server, '')
        string = string.replace(Modifiers.client, '')
        string = string.replace(Modifiers.external, '')
        string = string.replace(Modifiers.static, '')
        string = string.replace(Modifiers.const, '')
        string = string.replace(Modifiers.abstract, '')
        string = string.replace(Modifiers.private, '')
        string = string.replace(Modifiers.protected, '')
        string = string.replace(Modifiers.public, '')
        string = string.replace(Modifiers.virtual, '')
        return string
