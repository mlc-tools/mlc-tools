from ..core.Class import Class
from ..core.Object import Object
from ..utils.Error import Error
from .protocols import cpp_xml
from .protocols import cpp_json
from ..base.SerializerBase import SerializerBase
from .Writer import Writer

SERIALIZATION = 0
DESERIALIZATION = 1


class Serializer(SerializerBase):

    def __init__(self):
        SerializerBase.__init__(self)
        self.namespace = 'mg'

    def get_protocol(self, serialize_format):
        protocol = cpp_xml if serialize_format == 'xml' else cpp_json
        return protocol

    def get_parent_serialize_format(self):
        return '{}::{}({});\n'

    def get_serialization_function_args(self, serialize_type, format_serialization):
        def get_json(const):
            obj = Object()
            obj.type = 'Json::Value'
            obj.is_ref = True
            obj.is_const = const
            return obj

        def get_xml(const):
            obj = Object()
            obj.type = 'pugi::xml_node'
            obj.is_ref = const
            obj.is_const = const
            return obj

        if format_serialization == 'json' and serialize_type == SERIALIZATION:
            return ['json', get_json(False)]
        if format_serialization == 'json' and serialize_type == DESERIALIZATION:
            return ['json', get_json(True)]
        if format_serialization == 'xml' and serialize_type == SERIALIZATION:
            return ['xml', get_xml(False)]
        if format_serialization == 'xml' and serialize_type == DESERIALIZATION:
            return ['xml', get_xml(True)]

    def build_serialize_operation(self, obj, serialization_type, serialize_format):
        return self.build_serialize_operation_(obj.name, obj.type, obj.initial_value,
                                               serialization_type, obj.template_args, obj.is_pointer,
                                               obj.is_link, serialize_format)
    
    def build_serialize_operation_(self, obj_name, obj_type, obj_value, serialization_type, obj_template_args,
                                   obj_is_pointer, is_link, serialize_format):
        index = 0
        if obj_value is None:
            index = 1
    
        type_ = obj_type
        if self.parser.find_class(type_) and self.parser.find_class(type_).type == 'enum':
            string = self._build_serialize_operation_enum(obj_name, serialization_type)
            return string
        else:
            if obj_type not in self.parser.simple_types and type_ != 'list' and type_ != 'map':
                if is_link:
                    type_ = 'link'
                elif obj_is_pointer:
                    type_ = 'pointer'
                else:
                    type_ = 'serialized'
            template_args = list()
            if len(obj_template_args) > 0:
                if type_ == 'map':
                    if len(obj_template_args) != 2:
                        Error.exit(Error.MAP_TWO_ARGS, self.current_class.name, obj_name)
                    if serialization_type == SERIALIZATION:
                        return self.build_map_serialization(obj_name, obj_template_args, serialize_format)
                    if serialization_type == DESERIALIZATION:
                        return self.build_map_deserialization(obj_name, obj_template_args, serialize_format)
                else:
                    arg = obj_template_args[0]
                    assert (isinstance(arg, Object))
                    assert (isinstance(arg.type, str))
                    arg_type = arg.type
                    template_args.append(self.convert_type(arg_type))
                    type_cls = self.parser.find_class(arg.type)
                    if arg.is_link:
                        type_ = 'list<link>'
                    elif arg_type in self.parser.simple_types:
                        type_ = '{0}<{1}>'.format(type_, arg_type)
                    elif arg.is_pointer:
                        type_ = 'list<pointer>'
                    elif type_cls.type == 'enum':
                        type_ = 'list<enum>'
                    else:
                        type_ = '{0}<serialized>'.format(type_)
            if type_ not in self.serialize_protocol[serialization_type]:
                Error.exit(Error.UNKNOWN_SERIALISED_TYPE, type_, obj_type)
            pattern = self.serialize_protocol[serialization_type][type_][index]
            string = pattern.format(field=obj_name,
                                    type=self.convert_type(obj_type),
                                    default_value=obj_value,
                                    arg_0=template_args[0] if len(template_args) > 0 else '',
                                    arg_1=template_args[1] if len(template_args) > 1 else '',
                                    format=serialize_format,
                                    namespace=self.namespace)
        return string + '\n\n'
    
    def build_map_serialization(self, obj_name, obj_template_args, serialize_format):
        key = obj_template_args[0]
        value = obj_template_args[1]
        assert (isinstance(key, Object))
        assert (isinstance(value, Object))
        assert (isinstance(key.type, str))
        assert (isinstance(value.type, str))
        key_type = key.type
        value_type = value.type
        pattern = self.serialize_protocol[SERIALIZATION]['map'][0]
        a0 = obj_name
        a1 = self.build_serialize_operation_('key', key_type, None, SERIALIZATION, [],
                                             key.is_pointer, key.is_link, serialize_format)
        a2 = self.build_serialize_operation_('value', value_type, None, SERIALIZATION, value.template_args,
                                             value.is_pointer, value.is_link, serialize_format)
        return pattern.format(field=a0,
                              key_serialize=a1,
                              value_serialize=a2)
    
    def build_map_deserialization(self, obj_name, obj_template_args, serialize_format):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        key_type = key_type.name if isinstance(key_type, Class) else key_type
        value_type = value.name if isinstance(value, Class) else value.type
        value_type = value_type.name if isinstance(value_type, Class) else value_type
        pattern = self.serialize_protocol[DESERIALIZATION]['map'][0]
        if key.is_link:
            key_str = 'const {}* key(nullptr);'.format(key_type)
        elif key.is_pointer:
            key_str = 'auto key = make_intrusive<{}>();'.format(key_type)
        else:
            key_str = '{} key;'.format(self.convert_type(key_type))
    
        value_is_pointer = value.is_pointer if isinstance(value, Object) else False
        a0 = obj_name
        a1 = self.build_serialize_operation_('key', key_type, None, DESERIALIZATION, [],
                                             key.is_pointer, key.is_link, serialize_format)
        a2 = self.build_serialize_operation_('value', value_type, None, DESERIALIZATION, value.template_args,
                                             value_is_pointer, value.is_link, serialize_format)
        a3 = key_str
        a4 = Writer.write_named_object(value, '', False, False)
        if value.is_pointer:
            a4 = 'intrusive_ptr<{}>'.format(value_type)
        return pattern.format(field=a0,
                              key_serialize=a1,
                              value_serialize=a2,
                              key=a3,
                              value_type=a4)

    @staticmethod
    def convert_type(t):
        types = {
            'list': 'std::vector',
            'map': 'std::map',
            'string': 'std::string',
        }
        if t in types:
            return types[t]
        return t

    def _build_serialize_operation_enum(self, obj_name, serialization_type):
        pattern = self.serialize_protocol[serialization_type]['enum'][0]
        return pattern.format(field=obj_name, namespace=self.namespace) + '\n\n'
