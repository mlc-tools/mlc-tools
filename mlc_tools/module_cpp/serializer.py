from ..core.object import Object
from ..utils.error import Error
from .protocols import CPP_XML
from .protocols import CPP_JSON
from ..base.serializer_base import SerializerBase
from .writer import Writer

SERIALIZATION = 0
DESERIALIZATION = 1


class Serializer(SerializerBase):

    def __init__(self):
        SerializerBase.__init__(self)
        self.namespace = 'mg'

    def get_protocol(self, serialize_format):
        protocol = CPP_XML if serialize_format == 'xml' else CPP_JSON
        return protocol

    def get_parent_serialize_format(self):
        return '{}::{}({});\n'

    def get_serialization_function_args(self, serialize_type, serialize_format):
        def get_json():
            obj = Object()
            obj.type = 'SerializerJson' if serialize_type == SERIALIZATION else 'DeserializerJson'
            obj.is_ref = True
            return obj

        def get_xml():
            obj = Object()
            obj.type = 'SerializerXml' if serialize_type == SERIALIZATION else 'DeserializerXml'
            obj.is_ref = True
            return obj

        if serialize_format == 'json' and serialize_type == SERIALIZATION:
            return ['serializer', get_json()]
        if serialize_format == 'json' and serialize_type == DESERIALIZATION:
            return ['deserializer', get_json()]
        if serialize_format == 'xml' and serialize_type == SERIALIZATION:
            return ['serializer', get_xml()]
        if serialize_format == 'xml' and serialize_type == DESERIALIZATION:
            return ['deserializer', get_xml()]

    def build_serialize_operation(self, obj: Object, serialization_type, serialize_format):
        # return self.build_serialize_operation_(obj.name, obj.type, obj.initial_value,
        #                                        serialization_type, obj.template_args, obj.is_pointer,
        #                                        '', obj.is_link, serialize_format)
        result = ''
        if serialization_type == SERIALIZATION and obj.type in self.model.simple_types and obj.initial_value:
            result = 'serializer.serialize({name}, "{name}", {type}({value}));\n'
        elif serialization_type == SERIALIZATION:
            result = 'serializer.serialize({name}, "{name}");\n'
        elif serialization_type == DESERIALIZATION and obj.type in self.model.simple_types and obj.initial_value:
            result = 'deserializer.deserialize({name}, "{name}", {type}({value}));\n'
        elif serialization_type == DESERIALIZATION:
            result = 'deserializer.deserialize({name}, "{name}");\n'
        return result.format(name=obj.name, value=obj.initial_value, type=self.convert_type(obj.type))

    def build_serialize_operation_(self, obj_name, obj_type, obj_value, serialization_type, obj_template_args,
                                   obj_is_pointer, owner, is_link, serialize_format):
        index = 0
        if obj_value is None:
            index = 1
        type_ = obj_type
        if self.model.has_class(type_) and self.model.get_class(type_).type == 'enum':
            string = self._build_serialize_operation_enum(obj_name, serialization_type)
            return string

        if obj_type not in self.model.simple_types and type_ != 'list' and type_ != 'map':
            if is_link:
                type_ = 'link'
            elif obj_is_pointer:
                type_ = 'pointer'
            else:
                type_ = 'serialized'
        template_args = list()
        if obj_template_args:
            if type_ == 'map':
                if len(obj_template_args) != 2:
                    Error.exit(Error.MAP_TWO_ARGS, self.current_class.name, obj_name)
                if serialization_type == SERIALIZATION:
                    return self.build_map_serialization(obj_name, obj_template_args,
                                                        serialization_type, serialize_format)
                if serialization_type == DESERIALIZATION:
                    return self.build_map_deserialization(obj_name, obj_template_args, serialize_format)
            else:
                arg = obj_template_args[0]
                assert isinstance(arg, Object)
                assert isinstance(arg.type, str)
                arg_type = arg.type
                template_args.append(self.convert_type(arg_type))
                if arg.is_link:
                    type_ = 'list<link>'
                elif arg_type in self.model.simple_types:
                    type_ = '{0}<{1}>'.format(type_, arg_type)
                elif arg.is_pointer:
                    type_ = 'list<pointer>'
                elif self.model.has_class(arg.type) and self.model.get_class(arg.type).type == 'enum':
                    type_ = 'list<enum>'
                else:
                    type_ = '{0}<serialized>'.format(type_)
        if type_ not in self.serialize_protocol[serialization_type]:
            Error.exit(Error.UNKNOWN_SERIALISED_TYPE, type_, obj_type)
        pattern = self.serialize_protocol[serialization_type][type_][index]
        string = pattern.format(field=obj_name,
                                type=self.convert_type(obj_type),
                                default_value=obj_value,
                                arg_0=template_args[0] if template_args else '',
                                arg_1=template_args[1] if len(template_args) > 1 else '',
                                format=serialize_format,
                                namespace=self.namespace)
        return string + '\n\n'

    def build_map_serialization(self, obj_name, obj_template_args, serialization_type, serialize_format):
        key = obj_template_args[0]
        value = obj_template_args[1]
        assert isinstance(key, Object) and isinstance(value, Object)
        key_type = key.type
        value_type = value.type
        pattern = self.serialize_protocol[serialization_type]['map'][0]
        key_serialize = self.build_serialize_operation_('key', key_type, None, SERIALIZATION, [],
                                                        key.is_pointer, '', key.is_link, serialize_format)
        value_serialize = self.build_serialize_operation_('value', value_type, None, SERIALIZATION, value.template_args,
                                                          value.is_pointer, '', value.is_link, serialize_format)
        return pattern.format(field=obj_name,
                              key_serialize=key_serialize.strip(),
                              value_serialize=value_serialize.strip()) + '\n\n'

    def build_map_deserialization(self, obj_name, obj_template_args, serialize_format):
        key = obj_template_args[0]
        value = obj_template_args[1]
        assert isinstance(key, Object)
        assert isinstance(value, Object)
        assert isinstance(key.type, str)
        assert isinstance(value.type, str)
        key_type = key.type
        value_type = value.type
        pattern = self.serialize_protocol[DESERIALIZATION]['map'][0]
        if key.is_link:
            key_str = 'const {}* key(nullptr);'.format(key_type)
        elif key.is_pointer:
            key_str = 'auto key = make_intrusive<{}>();'.format(key_type)
        else:
            key_str = '{} key;'.format(self.convert_type(key_type))

        value_is_pointer = value.is_pointer
        key_serialize = self.build_serialize_operation_('key', key_type, None, DESERIALIZATION, [],
                                                        key.is_pointer, '', key.is_link, serialize_format)
        value_serialize = self.build_serialize_operation_('value', value_type, None, DESERIALIZATION,
                                                          value.template_args, value_is_pointer, '',
                                                          value.is_link, serialize_format)
        value_init = Writer.write_named_object(value, '', False, False)
        if value.is_pointer:
            value_init = 'intrusive_ptr<{}>'.format(value_type)
        return pattern.format(field=obj_name,
                              key_serialize=key_serialize.strip(),
                              value_serialize=value_serialize.strip(),
                              key=key_str,
                              value_type=value_init) + '\n\n'

    @staticmethod
    def convert_type(type_):
        types = {
            'list': 'std::vector',
            'map': 'std::map',
            'string': 'std::string',
        }
        if type_ in types:
            return types[type_]
        return type_

    def _build_serialize_operation_enum(self, obj_name, serialization_type):
        pattern = self.serialize_protocol[serialization_type]['enum'][0]
        return pattern.format(field=obj_name, namespace=self.namespace) + '\n\n'
