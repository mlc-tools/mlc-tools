from ..base import WriterBase
from .Serializer import Serializer


class Writer(WriterBase):

    def __init__(self, out_directory):
        WriterBase.__init__(self, out_directory)
        pass

    def write_class(self, cls):

        self.set_initial_values(cls)

        initialize_list = ''
        static_list = ''
        for obj in cls.members:
            if not obj.is_static:
                initialize_list += '        ' + self.write_object(obj) + '\n'
            else:
                static_list += '    ' + self.write_object(obj) + '\n'

        functions = ''
        for method in cls.functions:
            f = self.write_function(cls, method)
            functions += f

        imports = ''
        init_superclass = ''
        name = cls.name
        if cls.superclasses:
            name += '(' + cls.superclasses[0].name + ')'
            imports += 'from .{0} import {0}'.format(cls.superclasses[0].name)
            init_superclass = '        {0}.__init__(self)'.format(cls.superclasses[0].name)
        for obj in cls.members:
            type_class = self.parser.find_class(obj.type)
            if type_class and type_class.type == 'enum':
                imports += '\nfrom .{0} import {0}'.format(type_class.name)

        for import_line in imports.split('\n'):
            functions = functions.replace(import_line, '')
            initialize_list = initialize_list.replace(import_line, '')

        if not init_superclass and not initialize_list:
            init_superclass = '        pass'

        out = PATTERN_FILE.format(name=name,
                                  initialize_list=initialize_list,
                                  functions=functions,
                                  imports=imports,
                                  init_superclass=init_superclass,
                                  static_list=static_list)
        return [
            ('%s.py' % cls.name, self.prepare_file(out))
            ]

    @staticmethod
    def set_initial_values(cls):
        if cls.type == 'enum':
            for member in cls.members:
                if member.name == '_value' and member.initial_value is not None:
                    member.initial_value = cls.members[0].initial_value

    @staticmethod
    def write_function(cls, method):
        args = [x[0] for x in method.args]
        if not method.is_static:
            args.insert(0, 'self')
        args = ', '.join(args)

        if method.name == 'visit' \
                and method.args \
                and len(method.args[0]) > 1 \
                and cls.superclasses \
                and cls.superclasses[0].name.startswith('IVisitor'):
            ctx_name = method.args[0][1]
            ctx_name = ctx_name[0].lower() + ctx_name[1:]
            ctx_name = ctx_name.replace('*', '')
            method.name = 'visit_' + ctx_name

        text = PATTERN_METHOD.format(name=method.name,
                                     args=args,
                                     body=method.body)
        if method.is_static:
            text = '    @staticmethod' + text
        return text

    def write_object(self, obj):
        imports = ''
        if obj.name == 'from':
            obj.name = 'from_'
        value = obj.initial_value
        if value is None and not obj.is_pointer:
            type_ = obj.type
            if type_ == "string":
                value = '""'
            if type_ == "int":
                value = "0"
            if type_ == "float":
                value = "0"
            if type_ == "uint":
                value = "0"
            if type_ == "bool":
                value = "False"
            if type_ == "list":
                value = "[]"
            if type_ == "map":
                value = "{}"
            else:
                if self.parser.find_class(obj.type):
                    value = obj.type + '()'
                    imports += 'from .{0} import {0}\n        '.format(obj.type)
        if value and value.endswith('f'):
            value = value[0:-1] + '0'

        if obj.is_static:
            out = '{0} = {1}'
        else:
            out = 'self.{0} = {1}'
        out = imports + out.format(obj.name, Serializer.convert_initialize_value(value))
        return out if out.strip() else 'pass'

    @staticmethod
    def prepare_file(text):
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
        text = '# -*- coding: utf-8 -*-\n' + text
        return text


PATTERN_FILE = '''
import xml.etree.ElementTree as ET
import json
{imports}
class {name}:
{static_list}

    def __init__(self):
{init_superclass}
{initialize_list}
{functions}'''

PATTERN_METHOD = '''
    def {name}({args}):
{body}
        pass
'''
