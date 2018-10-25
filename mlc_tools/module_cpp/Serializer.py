import sys
from ..core.Function import Function
from ..core.Class import Class
from ..utils.Error import Error
from .protocols import cpp_xml
from .protocols import cpp_json

SERIALIZATION = 0
DESERIALIZATION = 1


class Serializer:
    serialize_protocol = {}

    def __init__(self):
        pass

    @staticmethod
    def get_protocol(serialize_format):
        protocol = cpp_xml if serialize_format == 'xml' else cpp_json
        if sys.version_info[0] == 3:
            protocol = protocol.replace('.iteritems()', '.items()')
        return protocol

    def generate_methods(self, parser):
        parser.load_default_serialize_protocol(self.get_protocol('xml'))
        Serializer.serialize_protocol = parser.serialize_protocol
        for cls in parser.classes:
            self.create_serialization_function(parser, cls, SERIALIZATION, 'xml')
            self.create_serialization_function(parser, cls, DESERIALIZATION, 'xml')

        parser.load_default_serialize_protocol(self.get_protocol('json'))
        Serializer.serialize_protocol = parser.serialize_protocol
        for cls in parser.classes:
            self.create_serialization_function(parser, cls, SERIALIZATION, 'json')
            self.create_serialization_function(parser, cls, DESERIALIZATION, 'json')

    @staticmethod
    def create_serialization_function(parser, cls, serialize_type, serialize_format):
        pass

        # print '{}::{}:\n{}\n\n'.format(cls.name, method.name, body)

    @staticmethod
    def build_map_serialization(parser, obj_name, obj_template_args, serialization_type, serialize_format):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        string = parser.serialize_protocol[serialization_type]['map'][0]
        a0 = obj_name
        a1 = Serializer.build_serialize_operation(parser, 'key', key_type, None, serialization_type,
                                                  key.template_args, False, '', key.is_link, serialize_format)
        a2 = Serializer.build_serialize_operation(parser, 'value', value_type, None, serialization_type,
                                                  value.template_args, value.is_pointer, '', value.is_link,
                                                  serialize_format)
        a1 = a1.split('\n')
        for index, a in enumerate(a1):
            a1[index] = '    ' + a
        a1 = '\n'.join(a1)
        a2 = a2.split('\n')
        for index, a in enumerate(a2):
            a2[index] = '    ' + a
        a2 = '\n'.join(a2)
        return string.format(field=a0,
                             key_serialize=a1,
                             value_serialize=a2,
                             owner='self.') + '\n'

    @staticmethod
    def convert_initialize_value(value):
        if value == 'true':
            return 'True'
        if value == 'false':
            return 'False'
        if value == 'nullptr':
            return 'None'
        if isinstance(value, str) and '::' in value:
            value = value.replace('::', '.')
        return value

    @staticmethod
    def get_serialization_function_args(format_serialization):
        return ['xml', ''] if format_serialization == 'xml' else ['dictionary', '']

    @staticmethod
    def build_serialize_operation(parser, obj_name, obj_type, obj_value, serialization_type, obj_template_args,
                                  obj_is_pointer, owner, is_link, serialize_format):
        index = 0
        if obj_value is None:
            index = 1

        type_ = obj_type
        cls = parser.find_class(type_)
        arg_0 = obj_template_args[0].type if len(obj_template_args) > 0 else 'unknown_arg'
        if cls and cls.type == 'enum':
            type_ = 'enum'
        elif obj_type not in parser.simple_types and type_ != "list" and type_ != "map":
            if is_link:
                type_ = 'link'
            elif obj_is_pointer:
                type_ = "pointer"
            else:
                type_ = "serialized"
        elif obj_type in parser.simple_types:
            type_ = obj_type
        else:
            if len(obj_template_args) > 0:
                if type_ == "map":
                    if len(obj_template_args) != 2:
                        Error.exit(Error.MAP_TWO_ARGS, cls.name, obj_name)
                    return Serializer.build_map_serialization(parser, obj_name,
                                                              obj_template_args, serialization_type, serialize_format)
                else:
                    arg = obj_template_args[0]
                    arg_type = arg.name if isinstance(arg, Class) else arg.type
                    if arg.is_link:
                        type_ = 'list<link>'
                    elif arg_type in parser.simple_types:
                        type_ = "list<{}>".format(arg_type)
                        obj_type = arg_type
                    elif arg.is_pointer:
                        type_ = "list<pointer>"
                    elif arg.type == 'enum':
                        type_ = 'list<string>'
                        arg_0 = 'string'
                    else:
                        type_ = "list<serialized>"
                        obj_type = arg_type
        string = Serializer.serialize_protocol[serialization_type][type_][index]
        string = string.format(field=obj_name,
                               type=obj_type,
                               default_value=obj_value,
                               owner=owner,
                               arg_0=arg_0,
                               format=serialize_format)

        return '        ' + string + '\n'
