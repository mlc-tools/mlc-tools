from Writer import Writer
from Function import Function
from Class import Class
from DataStorageCreators import DataStoragePythonXml
from DataStorageCreators import DataStoragePythonJson
import re

SERIALIZATION = 0
DESERIALIZATION = 1


def convertInitializeValue(value):
    if value == 'true':
        return 'True'
    if value == 'false':
        return 'False'
    return value


class WriterPython(Writer):

    def __init__(self, parser, serialize_format):
        Writer.__init__(self, parser, serialize_format)
        self.loaded_functions = {}

    def save_generated_classes(self, out_directory):
        Writer.save_generated_classes(self, out_directory)
        self.create_factory()
        self.create_visitor_acceptors()

    def write_class(self, cls, flags):
        global _pattern_file
        out = ""
        pattern = _pattern_file[self.serialize_format]
        self.current_class = cls

        if cls.type == 'enum':
            for member in cls.members:
                if member.initial_value is not None and member.name == '_value':
                    member.initial_value = cls.members[0].initial_value

        initialize_list = ''
        static_list = ''
        for object in cls.members:
            if not object.is_static:
                initialize_list += '        ' + self.write_object(object) + '\n'
            else:
                static_list += '    ' + self.write_object(object) + '\n'

        self.create_serialization_function(cls, SERIALIZATION)
        self.create_serialization_function(cls, DESERIALIZATION)
        functions = ''
        for function in cls.functions:
            f = self.write_function(cls, function)
            functions += f

        imports = ''
        init_behavior = ''
        name = cls.name
        if cls.behaviors:
            name += '(' + cls.behaviors[0].name + ')'
            imports += 'from {0} import {0}'.format(cls.behaviors[0].name)
            init_behavior = '        {0}.__init__(self)'.format(cls.behaviors[0].name)

        out = pattern.format(name, initialize_list, functions, imports, init_behavior, static_list)
        self.current_class = None
        return {flags: out}

    def write_function(self, cls, function):
        out = ''
        key = cls.name + '.' + function.name
        if key in self.loaded_functions:
            body = self.loaded_functions[key]
            out += '    def {0}{1}\n\n'.format(function.name, body)
            return out

        out = '''    def {0}({1}):
{2}
        \n'''
        name = function.name
        args = ', '.join([x[0] for x in function.args])
        if function.is_static:
            out = '    @staticmethod\n' + out
        else:
            if args:
                args = 'self, ' + args
            else:
                args = 'self'

        convert = self.current_class.name != 'DataStorage'
        if convert:
            ops = '\n'.join(function.operations)
            ops = convert_function_to_python(ops, self.parser)
        else:
            ops = '        ' + '\n        '.join(function.operations)

        if not ops.split():
            ops = '        pass'
        out = out.format(name, args, ops)

        return out

    def write_object(self, object):
        imports = ''
        if object.name == 'from':
            object.name = 'from_'
        value = object.initial_value
        if value is None and not object.is_pointer:
            type = object.type
            if type == "string":
                value = '""'
            if type == "int":
                value = "0"
            if type == "float":
                value = "0"
            if type == "uint":
                value = "0"
            if type == "bool":
                value = "False"
            if type == "list":
                value = "[]"
            if type == "map":
                value = "{}"
            else:
                if self.parser.find_class(object.type):
                    value = object.type + '()'
                    imports += 'from {0} import {0}\n        '.format(object.type)
        if value and value.endswith('f'):
            value = value[0:-1] + '0'

        if object.is_static:
            out = '{0} = {1}'
        else:
            out = 'self.{0} = {1}'
        out = out.format(object.name, convertInitializeValue(value))
        return imports + out

    def _getImports(self, cls):
        return ""

    def _get_filename_of_class(self, cls):
        return cls.name + ".py"

    def get_serialiation_function_args(self):
        if self.serialize_format == 'xml':
            return '(self, xml)'
        return '(self, dictionary)'

    def create_serialization_function(self, cls, serialize_type):
        function = Function()
        function.name = 'serialize' if serialize_type == SERIALIZATION else 'deserialize'
        for func in cls.functions:
            if func.name == function.name:
                return

        body = self.get_serialiation_function_args() + ':\n$(import)'
        if cls.behaviors:
            body += ('        {0}.{1}' + self.get_serialiation_function_args() + '\n').format(cls.behaviors[0].name,
                                                                                              function.name)
        for obj in cls.members:
            if obj.is_runtime:
                continue
            if obj.is_static:
                continue
            if obj.is_const and not obj.is_link:
                continue

            body += self.build_serialize_operation(obj.name, obj.type, convertInitializeValue(obj.initial_value),
                                                   serialize_type, obj.template_args, obj.is_pointer, 'self.', obj.is_link)
        use_factory = re.search(r'\bFactory\b', body) is not None
        use_data_storage = 'DataStorage.shared()' in body
        imports = ''
        if serialize_type == DESERIALIZATION:
            if use_factory:
                imports += '        from Factory import Factory\n'
            if use_data_storage:
                imports += '        from DataStorage import DataStorage\n'
        body = body.replace('$(import)', imports)

        body += '        return'
        self.loaded_functions[cls.name + '.' + function.name] = body
        cls.functions.append(function)

    def build_map_serialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args, serialization_type):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        str = self.serialize_protocol[serialization_type]['map'][0]
        _value_is_pointer = value.is_pointer
        a0 = obj_name
        a1 = self.build_serialize_operation('key', key_type, None, serialization_type, key.template_args, False, '', key.is_link)
        a2 = self.build_serialize_operation("value", value_type, None, serialization_type, value.template_args, _value_is_pointer, '', value.is_link)
        a1 = a1.split('\n')
        for index, a in enumerate(a1):
            a1[index] = '    ' + a
        a1 = '\n'.join(a1)
        a2 = a2.split('\n')
        for index, a in enumerate(a2):
            a2[index] = '    ' + a
        a2 = '\n'.join(a2)
        return str.format(a0, a1, a2, '{}', 'self.') + '\n'

    def build_serialize_operation(self, obj_name, obj_type, obj_value, serialization_type, obj_template_args,
                                  obj_is_pointer, owner='self.', is_link=False):
        index = 0
        if obj_value is None:
            index = 1

        type = obj_type
        if self.parser.find_class(type) and self.parser.find_class(type).type == 'enum':
            type = 'string'
        elif obj_type not in self.simple_types and type != "list" and type != "map":
            if is_link:
                type = 'link'
            elif obj_is_pointer:
                type = "pointer"
            else:
                type = "serialized"
        elif obj_type in self.simple_types:
            type = obj_type
        else:
            if len(obj_template_args) > 0:
                if type == "map":
                    if len(obj_template_args) != 2:
                        print "map should have 2 arguments"
                        exit - 1
                    return self.build_map_serialization(obj_name, obj_type, obj_value, obj_is_pointer,
                                                        obj_template_args, serialization_type)
                else:
                    arg = obj_template_args[0]
                    arg_type = arg.name if isinstance(arg, Class) else arg.type
                    if arg.is_link:
                        type = 'list<link>'
                    elif arg_type in self.simple_types:
                        type = "list<{}>".format(arg_type)
                        obj_type = arg_type
                    elif arg.is_pointer:
                        type = "list<pointer>"
                    elif arg.type == 'enum':
                        type = 'list<string>'
                    else:
                        type = "list<serialized>"
                        obj_type = arg_type
        fstr = self.serialize_protocol[serialization_type][type][index]
        str = fstr.format(obj_name, obj_type, obj_value, '{}', owner,
                          obj_template_args[0].type if len(obj_template_args) > 0 else 'unknown_arg')
        return '        ' + str + '\n'

    def save_config_file(self):
        buffer = 'MG_XML = 2\nMG_JSON = 1\n'
        buffer += 'MG_SERIALIZE_FORMAT = MG_' + self.serialize_format.upper()
        buffer += '\n'
        self.save_file('config.py', buffer)
        self.create_init_file()

    def create_factory(self):
        global _factory
        pattern = _factory[self.serialize_format]
        line = '        if type == "{0}": return {0}.{0}()\n'
        line_import = 'import {0}\n'
        creates = ''
        imports = ''
        for cls in self.parser.classes:
            creates += line.format(cls.name)
            imports += line_import.format(cls.name)
        factory = pattern.format(imports, creates)
        self.save_file('Factory.py', factory)

    def create_visitor_acceptors(self):
        pattern = _pattern_visitor
        line = '        elif ctx.__class__ == {0}:\n            self.visit_{1}(ctx)\n'
        line_import = 'from {0} import {0}\n'
        line_visit = '''\n    def visit_{0}(self, ctx):\n        pass\n'''
        base_visitors = {}
        for cls in self.parser.classes:
            if cls.is_visitor and (cls.behaviors and not cls.behaviors[0].is_visitor):
                base_visitors[cls] = []
        for cls in self.parser.classes:
            parent = cls.behaviors[0] if cls.behaviors else None
            while parent:
                if parent in base_visitors:
                    base_visitors[parent].append(cls)
                    break
                parent = parent.behaviors[0] if parent.behaviors else None
        for parent in base_visitors:
            lines = ''
            visits = ''
            imports = ''
            for cls in base_visitors[parent]:
                if self.parser.is_visitor(cls):
                    func_name = cls.name
                    func_name = func_name[0].lower() + func_name[1:]

                    lines += line.format(cls.name, func_name)
                    imports += line_import.format(cls.name)
                    visits += line_visit.format(func_name)
            name = 'IVisitor{}'.format(parent.name)
            body = pattern.format(imports, lines, visits, name)
            self.save_file(name + '.py', body)

    def create_data_storage_class(self, name, classes):
        if self.serialize_format == 'xml':
            return DataStoragePythonXml(name, classes, self.parser)
        else:
            return DataStoragePythonJson(name, classes, self.parser)

    def prepare_file(self, text):
        lines = text.split('\n')
        result = []
        tabs = False
        is_static = False
        for line in lines:
            if not line.split():
                continue
            if not line.startswith('    ') and tabs:
                result.extend(['', ''])
            elif line.startswith('    @'):
                is_static = True
                result.extend([''])
                result.append(line)
                continue
            elif not is_static:
                if line.startswith('class ') or line.startswith('def '):
                    result.extend(['', ''])
                elif line.strip().startswith('def '):
                    result.extend([''])
            result.append(line)
            if line.startswith('    '):
                tabs = True
            is_static = False
        result.append('')
        text = '\n'.join(result)
        if re.search(r'\bET\.', text):
            text = 'import xml.etree.ElementTree as ET\n' + text
        return text

    def create_data_storage(self):
        storage = self.create_data_storage_class('DataStorage', self.parser.classes)
        content = self.write_class(storage, 0)[0]
        content = self.prepare_file(content)
        self.save_file(storage.name + '.py', content)

    def create_init_file(self):
        self.save_file('__init__.py', '')

    def convert_to_enum(self, cls, use_type='string'):
        Writer.convert_to_enum(self, cls, use_type)

regs = [
    [re.compile('DataStorage::shared\(\).get<(\w+)>'), 'DataStorage::shared().get\\1'],
    [re.compile('for\s*\\(\s*\w+[\s&\*]*(\w+)\s*:\s*(.+)\s*\\)'), 'for \\1 in \\2:'],
    [re.compile('for\s*\\(\s*\w+\s*(\w+)=(\w+);\s*\w+<(\w+);\s*\\+\\+\w+\s*\\)'), 'for \\1 in xrange(\\2, \\3):'],
    [re.compile('for\s*\\(\s*\w+\s*(\w+)=(\w+);\s*\w+>(\w+);\s*--\w+\s*\\)'), 'for \\1 in xrange(\\2, \\3, -1):'],
    [re.compile('for\s*\\(\s*\w+\s*(\w+)=(\w+);\s*\w+<(\w+);\s*\w+\\+=(\w)\s*\\)'), 'for \\1 in xrange(\\2, \\3, \\4):'],
    [re.compile('for\s*\\(\s*\w+\s*(\w+)=(\w+);\s*\w+>(\w+);\s*\w+-=(\w)\s*\\)'), 'for \\1 in xrange(\\2, \\3, -\\4):'],
    [re.compile('for\s*\\(auto&&\s*\\[(\w+),\s*(\w+)\\]\s*:\s*(.+)\\)'), 'for \\1, \\2 in \\3.iteritems():'],
    [re.compile('if\s*\\(\s*(.+)\s*\\)'), 'if \\1:'],
    [re.compile('if\s*!(.+):'), 'if not (\\1):'],
    [re.compile('else if'), 'elif:'],
    [re.compile('else'), 'else:'],
    [re.compile('in_map\s*\\(\s*(.+),\s*(.+)\s*\\)'), '(\\1 in \\2)'],
    [re.compile('in_list\s*\\(\s*(.+),\s*(.+)\s*\\)'), '(\\1 in \\2)'],
    [re.compile('list_push\s*\\(\s*(.+),\s*(.+)\s*\\)'), '\\1.append(\\2)'],
    [re.compile('list_size\s*\\('), 'len('],
    [re.compile('map_size\s*\\('), 'len('],
    [re.compile('auto (\w+)'), '\\1'],
    [re.compile('string (\w+)'), '\\1'],
    [re.compile('int (\w+)'), '\\1'],
    [re.compile('float (\w+)'), '\\1'],
    [re.compile('bool (\w+)'), '\\1'],
    [re.compile('(\w)->'), '\\1.'],
    [re.compile('\+\+(\w+)'), '\\1 += 1'],
    [re.compile('delete (\w+);'), 'pass'],
    [re.compile('&(\w+)'), '\\1'],
    [re.compile('!(\w+)'), 'not \\1'],
    [re.compile('make_intrusive<(\w+)>\\(\\)'), '\\1()'],
    [re.compile('new\s*(\w+)\s*\\(\s*\\)'), '\\1()'],
    [re.compile('assert\\(.+\\);'), ''],
    [re.compile('([-0-9]+)\\.f'), '\\1.0'],
    [re.compile('([-0-9]+)\\.([-0-9]*)f'), '\\1.\\2'],
    [re.compile(';'), ''],
    [re.compile('([*+-/\s])log\\((.+?)\\)'), '\\1math.log(\\2)'],
]


def convert_function_to_python(func, parser):
    global regs
    repl = [
        ['this.', 'self.'],
        ['->', '.'],
        ['::', '.'],
        ['&&', ' and '],
        ['  and  ', ' and '],
        ['  or  ', ' or '],
        ['||', ' or '],
        ['true', 'True'],
        ['false', 'False'],
        ['nullptr', 'None'],
        ['std.round', 'round'],
        ['std.floor', 'math.floor'],
        ['std.min', 'min'],
        ['std.max', 'max'],
        ['!= None', 'is not None'],
        ['== None', 'is None'],
    ]

    for reg in regs:
        func = re.sub(reg[0], reg[1], func)

    for reg in repl:
        func = func.replace(reg[0], reg[1])

    def get_tabs(count):
        r = ''
        for i in xrange(count):
            r += '    '
        return r

    lines = func.split('\n')
    tabs = 2
    next_tab = False
    for i, line in enumerate(lines):
        if next_tab:
            tabs += 1
        if '{' in line:
            tabs += 1
            line = line.replace('{', '')
        if '}' in line:
            tabs -= 1
            line = line.replace('}', '')
        lines[i] = get_tabs(tabs) + line.strip()
        if next_tab:
            next_tab = False
            tabs -= 1
        if (line.startswith('for') or line.startswith('if') or line.startswith('else')) \
                and (i < len(lines) - 1 and '{' not in line and '{' not in lines[i + 1]):
            next_tab = True

    func = '\n'.join(lines)
    func = func.replace('\n    \n', '\n')
    func = func.replace('\n        \n', '\n')
    func = func.replace('\n            \n', '\n')
    func = func.replace('\n                \n', '\n')
    func = func.replace('\n                    \n', '\n')
    func = func.replace('\n                        \n', '\n')
    if 'DataStorage' in func:
        func = get_tabs(2) + 'from DataStorage import DataStorage\n' + func
    if re.search(r'\bFactory\b', func):
        func = get_tabs(2) + 'from Factory import Factory\n' + func
    for cls in parser.classes:
        if cls.name in func:
            func = get_tabs(2) + 'from {0} import {0}\n'.format(cls.name) + func
    if 'math.' in func:
        func = get_tabs(2) + 'import math\n' + func

    return func


_factory = {}
_factory['xml'] = '''import xml.etree.ElementTree as ET
{0}
class Factory:
    @staticmethod
    def build(type):
{1}
        return None
    @staticmethod
    def create_command(string):
        root = ET.fromstring(string)
        type = root.tag
        command = Factory.build(type)
        if command is not None:
            command.deserialize(root)
        return command

    @staticmethod
    def serialize_command(command):
        root = ET.Element(command.get_type())
        command.serialize(root)
        return ET.tostring(root)
'''
_factory['json'] = '''import json
{0}
class Factory:
    @staticmethod
    def build(type):
{1}
        return None
    @staticmethod
    def create_command(string):
        dictionary = json.loads(string)
        for key in dictionary:
            command = Factory.build(key)
            if command is not None:
                command.deserialize(dictionary[key])
            return command

    @staticmethod
    def serialize_command(command):
        js = dict()
        js[command.get_type()] = dict()
        command.serialize(js[command.get_type()])
        return json.dumps(js)
'''

_pattern_file = {}
_pattern_file['xml'] = '''
{3}\nclass {0}:
{5}

    def __init__(self):\n{4}\n{1}\n        pass
{2}'''

_pattern_file['json'] = '''import json
{3}
class {0}:
{5}

    def __init__(self):\n{4}\n{1}\n        pass
{2}'''

_pattern_visitor = '''{0}\nclass {3}:
    def __init__(self):\n        self.response = None
    def visit(self, ctx):\n        if ctx is None:\n            return
{1}\n{2}
'''
