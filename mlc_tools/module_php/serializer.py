import sys
from ..base.serializer_base import SerializerBase
from ..core.object import Object, Objects
from ..utils.error import Error
from .protocols import PHP_XML
from .protocols import PHP_JSON
from .regex import RegexPatternPhp

SERIALIZATION = 0
DESERIALIZATION = 1


class Serializer(SerializerBase):

    def __init__(self):
        SerializerBase.__init__(self)

    def get_protocol(self, serialize_format):
        protocol = PHP_XML if serialize_format == 'xml' else PHP_JSON
        if sys.version_info[0] == 3:
            protocol = protocol.replace('.iteritems()', '.items()')
        return protocol

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
        return 'parent::{1}({2});\n'

    def build_map_serialization(self, obj_name, obj_template_args, serialization_type, serialize_format):
        key = obj_template_args[0]
        value = obj_template_args[1]
        assert (isinstance(key, Object))
        assert (isinstance(value, Object))
        assert (isinstance(key.type, str))
        assert (isinstance(value.type, str))
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

    @staticmethod
    def convert_initialize_value(value):
        assert (value is None or isinstance(value, str))

        if value is None or value == 'nullptr' or value == 'None':
            value = 'null'
        if value and value.startswith('this'):
            value = '$' + value
        value = RegexPatternPhp.INITIALIZE[0].sub(RegexPatternPhp.INITIALIZE[1], value)
        return value

    def get_serialization_function_args(self, serialize_type, serialize_format):
        return ['xml', Objects.VOID] if serialize_format == 'xml' else ['json', Objects.VOID]

    def build_serialize_operation(self, obj, serialization_type, serialize_format):
        return self.build_serialize_operation_(obj.name, obj.type, obj.initial_value,
                                               serialization_type, obj.template_args, obj.is_pointer, '$this->',
                                               obj.is_link, serialize_format)

    def build_serialize_operation_(self, obj_name, obj_type, obj_value, serialization_type, obj_template_args,
                                   obj_is_pointer, owner, is_link, serialize_format):
        index = 0
        if obj_value is None:
            index = 1

        type_ = obj_type
        cls = self.model.get_class(type_)
        arg_0 = obj_template_args[0].type if obj_template_args else 'unknown_arg'
        if cls and cls.type == 'enum':
            type_ = 'enum'
        elif obj_type not in self.model.simple_types and type_ != "list" and type_ != "map":
            if is_link:
                type_ = 'link'
            elif obj_is_pointer:
                type_ = "pointer"
            else:
                type_ = "serialized"
        elif obj_type in self.model.simple_types:
            type_ = obj_type
        else:
            if obj_template_args:
                if type_ == "map":
                    if len(obj_template_args) != 2:
                        Error.exit(Error.MAP_TWO_ARGS, cls.name, obj_name)
                    return self.build_map_serialization(obj_name, obj_template_args,
                                                        serialization_type, serialize_format)
                else:
                    arg = obj_template_args[0]
                    assert (isinstance(arg, Object))
                    assert (isinstance(arg.type, str))
                    arg_type = arg.type
                    type_cls = self.model.get_class(arg.type)
                    if arg.is_link:
                        type_ = 'list<link>'
                    elif arg_type in self.model.simple_types:
                        type_ = "list<{}>".format(arg_type)
                        obj_type = arg_type
                    elif arg.is_pointer:
                        type_ = "list<pointer>"
                    elif type_cls.type == 'enum':
                        type_ = 'list<string>'
                        arg_0 = 'string'
                    else:
                        type_ = "list<serialized>"
                        obj_type = arg_type
        obj_value = Serializer.convert_initialize_value(obj_value)
        string = self.serialize_protocol[serialization_type][type_][index]
        string = string.format(field=obj_name,
                               type=obj_type,
                               default_value=obj_value,
                               owner=owner,
                               arg_0=arg_0,
                               format=serialize_format)

        return string + '\n'
