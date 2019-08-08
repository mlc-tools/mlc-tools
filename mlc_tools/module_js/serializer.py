from ..base.serializer_base import SerializerBase
from ..core.object import Object, Objects
from .protocols import JS_JSON
from .regex import RegexPatternJs


class Serializer(SerializerBase):

    def __init__(self):
        SerializerBase.__init__(self)

    def get_protocol(self, serialize_format):
        assert serialize_format == 'json'
        return JS_JSON

    def create_serialization_function(self, cls, serialize_type, serialize_format):
        return SerializerBase.create_serialization_function(self, cls, serialize_type, serialize_format)

    def get_parent_serialize_format(self):
        return '{0}.prototype.{1}.call(this, {2});\n'

    def build_map_serialization(self, obj_name, obj_template_args, serialization_type, serialize_format):
        key = obj_template_args[0]
        value = obj_template_args[1]
        assert isinstance(key, Object) and isinstance(value, Object)
        key_type = key.type
        value_type = value.type
        pattern = self.serialize_protocol[serialization_type]['map'][0]
        value_is_pointer = value.is_pointer

        def get_create_type_operation(type_):
            types = {
                'list': '[]',
                'map': '{}',
            }
            return types[type_] if type_ in types else 'new ' + type_

        if value_type not in self.model.simple_types:
            value_declaration = 'let value = {}();'.format(get_create_type_operation(value_type))
        else:
            value_declaration = ''
        key_serialize = self.build_serialize_operation_('key', key_type, None, serialization_type, key.template_args,
                                                        False, '', key.is_link, serialize_format)
        value_serialize = self.build_serialize_operation_('value', value_type, None, serialization_type,
                                                          value.template_args,
                                                          value_is_pointer, '', False, serialize_format)
        key_serialize = key_serialize.split('\n')
        for index, line in enumerate(key_serialize):
            key_serialize[index] = line
        key_serialize = '\n'.join(key_serialize)
        value_serialize = value_serialize.split('\n')
        for index, line in enumerate(value_serialize):
            value_serialize[index] = line
        value_serialize = '\n'.join(value_serialize)
        return pattern.format(field=obj_name,
                              key_serialize=key_serialize,
                              value_serialize=value_serialize,
                              key='{}',
                              owner='this.',
                              value=value_declaration,
                              value_type=value.type) + '\n'

    def convert_initialize_value(self, value):
        assert value is None or isinstance(value, str)

        if value in [None, 'nullptr', 'None']:
            value = 'null'
        value = value.replace('::', '.')
        value = RegexPatternJs.INITIALIZE[0].sub(RegexPatternJs.INITIALIZE[1], value)
        return value

    def get_serialization_function_args(self, serialize_type, serialize_format):
        return ['json', Objects.VOID]

    def build_serialize_operation(self, obj, serialization_type, serialize_format):
        return self.build_serialize_operation_(obj.name, obj.type, obj.initial_value,
                                               serialization_type, obj.template_args, obj.is_pointer, 'this.',
                                               obj.is_link, serialize_format)

    def finalize_serialize_operation(self, string):
        return string + '\n'
