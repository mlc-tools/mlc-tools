from ..base import WriterBase
from .serializer import Serializer


class Writer(WriterBase):

    def __init__(self, out_directory):
        WriterBase.__init__(self, out_directory)

    def write_class(self, cls):
        self.set_initial_values(cls)

        imports_in_static = []
        imports_in_ctr = []
        initialize_list = ''
        static_list = ''
        slots = []
        for obj in cls.members:
            if not obj.is_static:
                v, i = self.write_object(obj)
                initialize_list += '        ' + v + '\n'
                imports_in_ctr.extend(i)
                slots.append('"%s"' % obj.name)
            else:
                v, i = self.write_object(obj)
                static_list += '    ' + v + '\n'
                imports_in_static.extend(i)
        slots = '__slots__ = [' + ', '.join(slots) + ']'

        imports_in_ctr = [' ' * 8 + x for x in imports_in_ctr]
        imports_in_static = [' ' * 4 + x for x in imports_in_static]
        initialize_list = '\n'.join(imports_in_ctr) + '\n' + initialize_list
        static_list = '\n'.join(imports_in_static) + '\n' + static_list

        if not initialize_list.strip():
            initialize_list = ' ' * 8 + 'pass'

        functions = ''
        for method in cls.functions:
            text = self.write_function(method)
            functions += text

        imports = 'from .common import *\n'
        if not cls.type == 'enum' and cls.name != 'BaseEnum':
            imports += 'from .SerializerXml import SerializerXml\n'
            imports += 'from .DeserializerXml import DeserializerXml\n'
            imports += 'from .SerializerJson import SerializerJson\n'
            imports += 'from .DeserializerJson import DeserializerJson\n'
            imports += 'from .IntrusivePtr import *\n'
        init_superclass = ''
        name = cls.name
        if cls.superclasses:
            superclass_name = cls.superclasses[0].name
            imports += 'from .{0} import {0}'.format(cls.superclasses[0].name)
            init_superclass = '        {0}.__init__(self)'.format(cls.superclasses[0].name)
        else:
            superclass_name = 'object'
        name += '(' + superclass_name + ')'

        for obj in cls.members:
            type_class = self.model.get_class(obj.type) if self.model.has_class(obj.type) else None
            if type_class is not None and type_class.type == 'enum':
                imports += '\nfrom .{0} import {0}'.format(type_class.name)

        for import_line in imports.split('\n'):
            functions = functions.replace(import_line, '')
            initialize_list = initialize_list.replace(import_line, '')

        if not init_superclass and not initialize_list:
            init_superclass = '        pass'

        constructor_args, constructor_body = self.get_constructor_data(cls)
        out = PATTERN_FILE.format(name=name,
                                  initialize_list=initialize_list,
                                  functions=functions,
                                  imports=imports,
                                  init_superclass=init_superclass,
                                  static_list=static_list,
                                  slots=slots,
                                  constructor_args=constructor_args,
                                  constructor_body=constructor_body)
        return [
            ('%s.py' % cls.name, self.prepare_file(out))
        ]

    def write_object(self, obj):
        imports = []
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
            if type_ in ["uint", 'unsigned']:
                value = "0"
            if type_ == "bool":
                value = "False"
            if type_ == "list":
                value = "[]"
            if type_ == "map":
                value = "{}"
            else:
                if self.model.has_class(obj.type) and self.current_class.name != obj.type:
                    value = obj.type + '()'
                    tabs = ' ' * (4 if obj.is_static else 8)
                    imports.append(f'from .{obj.type} import {obj.type}')
        if value and value.endswith('f'):
            value = value[0:-1] + '0'

        if obj.is_static:
            out = '{0} = {1}'
        else:
            out = 'self.{0} = {1}'
        out = out.format(obj.name, Serializer().convert_initialize_value(value))
        return out, imports

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
        text = '# -*- coding: utf-8 -*-\n' + text
        return WriterBase.prepare_file(self, text)

    def get_method_arg_pattern(self, obj):
        return '{name}={value}' if obj.initial_value is not None else '{name}'

    def get_method_pattern(self, method):
        return PATTERN_METHOD

    def get_required_args_to_function(self, method):
        if not method or not method.is_static:
            return 'self'
        return None

    def get_nullptr_string(self):
        return 'None'

    def add_static_modifier_to_method(self, text):
        return '    @staticmethod' + text


PATTERN_FILE = '''
import xml.etree.ElementTree as ET
import json
from .mg_extensions import *
{imports}
class {name}:
{static_list}
    {slots}
    def __init__({constructor_args}):
{init_superclass}
{initialize_list}
{constructor_body}
    def __hash__(self):
        return id(self)
{functions}'''

PATTERN_METHOD = '''
    def {name}({args}):
{body}
'''
