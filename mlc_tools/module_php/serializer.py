from ..base.serializer_base import SerializerBase, DESERIALIZATION
from ..core.object import Object, Objects
from .protocols import PHP_XML
from .protocols import PHP_JSON
from .regex import RegexPatternPhp


class Serializer(SerializerBase):

    def __init__(self):
        SerializerBase.__init__(self)

    def get_protocol(self, serialize_format):
        return PHP_XML if serialize_format == 'xml' else PHP_JSON

    def create_serialization_function(self, cls, serialize_type, serialize_format):
        method = SerializerBase.create_serialization_function(self, cls, serialize_type, serialize_format)

        use_data_storage = 'DataStorage::shared()' in method.body
        use_factory = 'Factory::shared()' in method.body
        imports = ''
        if serialize_type == DESERIALIZATION:
            if use_factory:
                imports += 'require_once "Factory.php";\n'
            if use_data_storage:
                imports += 'require_once "DataStorage.php";\n'
        if imports:
            method.body = imports + method.body
        return method.body

    def get_parent_serialize_format(self):
        return 'parent::{1}(${2});\n'

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
                'list': 'array',
                'map': 'array',
            }
            return types[type_] if type_ in types else 'new ' + type_

        if value_type not in self.model.simple_types:
            value_declaration = '$value = {}();'.format(get_create_type_operation(value_type))
        else:
            value_declaration = ''
        key_serialize = self.build_serialize_operation_('key', key_type, None, serialization_type, key.template_args,
                                                        False, '$', key.is_link, serialize_format)
        value_serialize = self.build_serialize_operation_('value', value_type, None, serialization_type,
                                                          value.template_args,
                                                          value_is_pointer, '$', False, serialize_format)
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
                              owner='$this->',
                              value=value_declaration) + '\n'

    def convert_initialize_value(self, value):
        assert value is None or isinstance(value, str)

        if value in [None, 'nullptr', 'None']:
            value = 'null'
        if value and value.startswith('this'):
            value = '$' + value
        value = RegexPatternPhp.INITIALIZE[0].sub(RegexPatternPhp.INITIALIZE[1], value)
        return value

    def get_serialization_function_args(self, serialize_type, serialize_format):
        return ['xml', Objects.VOID] if serialize_format == 'xml' else ['json', Objects.VOID]

    def build_serialize_operation(self, obj, serialization_type, serialize_format):
        value = self.build_serialize_operation_(obj.name, obj.type, obj.initial_value,
                                                serialization_type, obj.template_args, obj.is_pointer, '$this->',
                                                obj.is_link, serialize_format)
        value = value.replace('(int64_t)', '(int)')
        value = value.replace('(uint)', '(int)')
        value = value.replace('(uint64_t)', 'int)')
        return value

    def finalize_serialize_operation(self, string):
        return string + '\n'
