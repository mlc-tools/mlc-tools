import sys
from ..base.serializer_base import SerializerBase, DESERIALIZATION
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

        use_factory = RegexPatternPython.FACTORY.search(method.body) is not None
        use_data_storage = 'DataStorage.shared()' in method.body
        imports = ''
        if serialize_type == DESERIALIZATION:
            if use_factory:
                imports += '        from .Factory import Factory\n'
            if use_data_storage:
                imports += '        from .DataStorage import DataStorage\n'
        if imports:
            method.body = imports + method.body
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
        assert (value is None or isinstance(value, str))
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
        return ['xml', Objects.VOID] if serialize_format == 'xml' else ['dictionary', Objects.VOID]

    def build_serialize_operation(self, obj, serialization_type, serialize_format):
        return self.build_serialize_operation_(obj.name, obj.type, obj.initial_value,
                                               serialization_type, obj.template_args, obj.is_pointer, 'self.',
                                               obj.is_link, serialize_format)

    def finalize_serialize_operation(self, string):
        for pattern in RegexPatternPython.PEP8:
            string = pattern[0].sub(pattern[1], string)
        return '        ' + string + '\n'
