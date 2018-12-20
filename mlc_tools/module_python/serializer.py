import sys
from ..base.serializer_base import SerializerBase
from ..core.object import Object, Objects
from ..utils.error import Error
from .regex import RegexPatternPython
from .protocols import PY_XML
from .protocols import PY_JSON

SERIALIZATION = 0
DESERIALIZATION = 1


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
        assert (isinstance(key, Object))
        assert (isinstance(value, Object))
        assert (isinstance(key.type, str))
        assert (isinstance(value.type, str))
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

    @staticmethod
    def convert_initialize_value(value):
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
                    elif type_cls and type_cls.type == 'enum':
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

        for pattern in RegexPatternPython.PEP8:
            string = pattern[0].sub(pattern[1], string)
        return '        ' + string + '\n'
