from ..Function import Function
from ..Class import Class
from ..Error import Error
from .regex import RegexPatternPython


SERIALIZATION = 0
DESERIALIZATION = 1


class Serializer:
    serialize_protocol = {}
    current_class = None

    def __init__(self):
        pass

    def generate_methods(self, parser):
        parser.load_default_serialize_protocol('py', 'xml')
        Serializer.serialize_protocol = parser.serialize_protocol
        for cls in parser.classes:
            Serializer.current_class = cls
            self.create_serialization_function(parser, cls, SERIALIZATION, 'xml')
            self.create_serialization_function(parser, cls, DESERIALIZATION, 'xml')

        parser.load_default_serialize_protocol('py', 'json')
        Serializer.serialize_protocol = parser.serialize_protocol
        for cls in parser.classes:
            Serializer.current_class = cls
            self.create_serialization_function(parser, cls, SERIALIZATION, 'json')
            self.create_serialization_function(parser, cls, DESERIALIZATION, 'json')

    @staticmethod
    def create_serialization_function(parser, cls, serialize_type, serialize_format):
        method = Function()
        method.name = ('serialize_' if serialize_type == SERIALIZATION else 'deserialize_') + serialize_format
        method.translated = True
        for func in cls.functions:
            if func.name == method.name:
                return

        method.args.append(Serializer.get_serialization_function_args(serialize_format))
        body = '$(import)'
        if cls.superclasses:
            call_parent = '{}.{}(self, {})'.format(cls.superclasses[0].name, method.name, method.args[0][0])
            body += '        {}\n'.format(call_parent)
        for obj in cls.members:
            if obj.is_runtime:
                continue
            if obj.is_static:
                continue
            if obj.is_const and not obj.is_link:
                continue

            init_value = Serializer.convert_initialize_value(obj.initial_value)
            body += Serializer.build_serialize_operation(parser, obj.name, obj.type, init_value, serialize_type,
                                                         obj.template_args, obj.is_pointer, 'self.', obj.is_link,
                                                         serialize_format)
        use_factory = RegexPatternPython.FACTORY.search(body) is not None
        use_data_storage = 'DataStorage.shared()' in body
        imports = ''
        if serialize_type == DESERIALIZATION:
            if use_factory:
                imports += '        from .Factory import Factory\n'
            if use_data_storage:
                imports += '        from .DataStorage import DataStorage\n'
        body = body.replace('$(import)', imports)

        method.body = body
        cls.functions.append(method)

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
        a2 = Serializer.build_serialize_operation(parser, "value", value_type, None, serialization_type,
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
                        Error.exit(Error.MAP_TWO_ARGS, Serializer.current_class.name, obj_name)
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

        for pattern in RegexPatternPython.PEP8:
            string = pattern[0].sub(pattern[1], string)
        return '        ' + string + '\n'
