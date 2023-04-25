from ..base.model import SerializeFormat, Model
from ..core.class_ import Class
from ..core.function import Function
from ..core.object import Objects, Object
from ..utils.error import Error

SERIALIZATION = 0
DESERIALIZATION = 1


class SerializerBase(object):

    def __init__(self):
        self.serialize_protocol = {}
        self.model: Model or None = None
        self.current_class: Class or None = None

    def generate_methods(self, model: Model):
        self.model = model

        formats = SerializeFormat.get_all()
        for serialize_format, string_format in formats:
            if model.serialize_formats & serialize_format:
                model.parser.load_default_serialize_protocol(self.get_protocol(string_format))
                self.serialize_protocol = model.serialize_protocol
                for cls in model.classes:
                    if cls.type == 'enum':
                        continue
                    if cls.name == 'BaseEnum':
                        continue
                    self.current_class = cls
                    self.create_serialization_function(cls, SERIALIZATION, string_format)
                    self.create_serialization_function(cls, DESERIALIZATION, string_format)

    def create_serialization_function(self, cls, serialize_type, serialize_format):
        method = Function()
        method.name = ('serialize_' if serialize_type == SERIALIZATION else 'deserialize_') + serialize_format
        method.translated = True
        method.return_type = Objects.VOID
        method.is_virtual = len(cls.superclasses) > 0 or len(cls.subclasses) > 0
        method.is_const = serialize_type == SERIALIZATION
        for func in cls.functions:
            if func.name == method.name:
                return method

        method.args.append(self.get_serialization_function_args(serialize_type, serialize_format))
        body = ''
        if cls.superclasses and cls.type != 'enum' and cls.superclasses[0].type != 'enum':
            parent_call = self.get_parent_serialize_format()
            body += parent_call.format(cls.superclasses[0].name, method.name, method.args[0][0])
        for obj in cls.members:
            if obj.is_runtime:
                continue
            if obj.is_static:
                continue
            if obj.is_const and not obj.is_link:
                continue
            body += self.build_serialize_operation(obj, serialize_type, serialize_format)
        method.body = body.rstrip()
        cls.functions.append(method)
        return method

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    def get_protocol(self, serialize_format):
        assert False and "override me"

    def get_parent_serialize_format(self):
        assert False and "override me"

    def get_serialization_function_args(self, serialize_type, serialize_format):
        assert False and "override me"

    def build_serialize_operation(self, obj, serialization_type, serialize_format):
        assert False and "override me"

    def build_map_serialization(self, obj_name, obj_template_args, serialization_type, serialize_format):
        assert False and "override me"

    def finalize_serialize_operation(self, string):
        assert False and "override me"

    def convert_initialize_value(self, value):
        assert False and "override me"
    # pylint: enable=no-self-use
    # pylint: enable=unused-argument

    def build_serialize_operation_(self, obj_name, obj_type, obj_value, serialization_type, obj_template_args,
                                   obj_is_pointer, owner, is_link, serialize_format):
        index = 0
        if obj_value is None:
            index = 1

        type_ = obj_type
        cls = self.model.get_class(type_) if self.model.has_class(type_) else None
        arg_0 = obj_template_args[0].type if obj_template_args else 'unknown_arg'
        if cls is not None and cls.type == 'enum':
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

                arg = obj_template_args[0]
                assert isinstance(arg, Object)
                assert isinstance(arg.type, str)
                arg_type = arg.type
                type_cls = self.model.get_class(arg.type) if self.model.has_class(arg.type) else None
                if arg.is_link:
                    type_ = 'list<link>'
                elif arg_type in self.model.simple_types:
                    type_ = "list<{}>".format(arg_type)
                    obj_type = arg_type
                elif arg.is_pointer:
                    type_ = "list<pointer>"
                elif type_cls is not None and type_cls.type == 'enum':
                    type_ = 'list<string>'
                    arg_0 = 'string'
                else:
                    type_ = "list<serialized>"
                    obj_type = arg_type

        obj_value = self.convert_initialize_value(obj_value)
        string = self.serialize_protocol[serialization_type][type_][index]
        string = string.format(field=obj_name,
                               type=obj_type,
                               default_value=obj_value,
                               owner=owner,
                               arg_0=arg_0,
                               format=serialize_format)

        return self.finalize_serialize_operation(string)
