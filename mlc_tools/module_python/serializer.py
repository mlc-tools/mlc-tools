import sys
from ..base.serializer_base import SerializerBase, DESERIALIZATION, SERIALIZATION
from ..core.object import Object, Objects
from .regex import RegexPatternPython
from .protocols import PY_XML
from .protocols import PY_JSON


class Serializer(SerializerBase):

    def __init__(self):
        SerializerBase.__init__(self)

    def get_protocol(self, serialize_format):
        protocol = PY_XML if serialize_format == 'xml' else PY_JSON
        if sys.version_info[0] == 3:
            protocol = protocol.replace('.iteritems()', '.items()')
        return protocol

    def create_serialization_function(self, cls, serialize_type, serialize_format):
        method = SerializerBase.create_serialization_function(self, cls, serialize_type, serialize_format)

        if 'import' in method.body:
            imports = []
            body = []
            lines = method.body.split('\n')
            for line in lines:
                if line.startswith('        from '):
                    if line not in imports:
                        imports.append(line)
                elif line.strip():
                    body.append(line)
            method.body = '\n'.join(imports) + '\n' + '\n'.join(body)

        use_factory = RegexPatternPython.FACTORY.search(method.body) is not None
        use_data_storage = 'DataStorage.shared()' in method.body
        imports = ''
        if serialize_type == DESERIALIZATION:
            imports += '        from .Meta import Meta\n'
            for member in cls.members:
                if self.model.has_class(member.type) and member.type != cls.name:
                    line = '        from .{0} import {0}\n'.format(member.type)
                    if line not in imports and line not in method.body:
                        imports += line
            if use_factory:
                imports += '        from .Factory import Factory\n'
            if use_data_storage:
                imports += '        from .DataStorage import DataStorage\n'
        if imports and method.body:
            method.body = imports + method.body
        elif not method.body:
            method.body = '        pass'
        method.body = method.body.replace('::', '.')
        return method.body

    def get_parent_serialize_format(self):
        return '        {}.{}(self, {})\n'

    def build_map_serialization(self, obj_name, obj_template_args, serialization_type, serialize_format):
        key = obj_template_args[0]
        value = obj_template_args[1]
        assert isinstance(key, Object) and isinstance(value, Object)
        key_type = key.type
        value_type = value.type
        string = self.model.serialize_protocol[serialization_type]['map'][0]
        key_serialize = self.build_serialize_operation_('key', key_type, None, serialization_type,
                                                        key.template_args, False, '', key.is_link, serialize_format)
        value_serialize = self.build_serialize_operation_('value', value_type, None, serialization_type,
                                                          value.template_args, value.is_pointer, '', value.is_link,
                                                          serialize_format)
        key_serialize = key_serialize.split('\n')
        for index, line in enumerate(key_serialize):
            key_serialize[index] = '    ' + line
        key_serialize = '\n'.join(key_serialize)
        value_serialize = value_serialize.split('\n')
        for index, line in enumerate(value_serialize):
            value_serialize[index] = '    ' + line
        value_serialize = '\n'.join(value_serialize)
        return string.format(field=obj_name,
                             key_serialize=key_serialize,
                             value_serialize=value_serialize,
                             owner='self.') + '\n'

    def convert_initialize_value(self, value):
        assert value is None or isinstance(value, str)
        if value is None:
            return None

        if value == 'true':
            return 'True'
        if value == 'false':
            return 'False'
        if value == 'nullptr':
            return 'None'
        if '::' in value:
            value = value.replace('::', '.')
        return value

    def get_serialization_function_args(self, serialize_type, serialize_format):
        return ['serializer', Objects.VOID]

    def build_serialize_operation(self, obj, serialization_type, serialize_format):
        if serialization_type == SERIALIZATION:
            if obj.initial_value is not None:
                value = self.convert_initialize_value(obj.initial_value)
                return '\n        serializer.serialize(self.{0}, "{0}", {1})'.format(obj.name, value)
            else:
                return '\n        serializer.serialize(self.{0}, "{0}")'.format(obj.name)
        if serialization_type == DESERIALIZATION:
            meta, imports = self.create_meta_class(obj)
            imports = '\n'.join(['        from .{0} import {0}'.format(x) for x in imports if x != self.current_class.name]) if imports else ''
            if obj.initial_value:
                value = self.convert_initialize_value(obj.initial_value)
                return '\n{2}\n        self.{0} = serializer.deserialize("{0}", {1}, {3})'.format(obj.name, meta, imports, value)
            else:
                return '\n{2}\n        self.{0} = serializer.deserialize("{0}", {1})'.format(obj.name, meta, imports)
        return self.build_serialize_operation_(obj.name, obj.type, obj.initial_value,
                                               serialization_type, obj.template_args, obj.is_pointer, 'self.',
                                               obj.is_link, serialize_format)

    def finalize_serialize_operation(self, string):
        for pattern in RegexPatternPython.PEP8:
            string = pattern[0].sub(pattern[1], string)
        return '        ' + string + '\n'

    def create_meta_class(self, obj: Object) -> (str, []):
        types = {
            'string': 'str',
            'map': 'dict',
            'int': 'int',
            'uint': 'int',
            'unsigned': 'int',
            'int64_t': 'int',
            'uint64_t': 'int',
            'float': 'float',
            'double': 'float',
            'bool': 'bool',
        }
        if obj.is_link:
            return 'Meta(DataWrapper, {})'.format(obj.type), ['DataWrapper', obj.type]
        elif obj.is_pointer:
            return 'Meta(IntrusivePtr, {})'.format(obj.type), ['IntrusivePtr', obj.type]
        elif not obj.template_args:
            if obj.type in types:
                return types[obj.type], []
            return obj.type, [obj.type]
        args = [self.create_meta_class(x) for x in obj.template_args]
        type = types[obj.type] if obj.type in types else obj.type
        meta = 'Meta({}, {})'.format(type, ', '.join([x[0] for x in args]))
        args_ = []
        for x in args:
            if x[1]:
                args_.extend(x[1])
        args = [obj.type] if self.model.has_class(obj.type) else []
        args.extend(args_)
        return meta, args
