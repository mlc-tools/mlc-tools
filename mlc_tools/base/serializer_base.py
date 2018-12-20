from ..core.function import Function
from ..core.object import Objects

SERIALIZATION = 0
DESERIALIZATION = 1


class SerializerBase(object):

    def __init__(self):
        self.serialize_protocol = {}
        self.model = None
        self.current_class = None

    def generate_methods(self, model):
        self.model = model
        model.parser.load_default_serialize_protocol(self.get_protocol('xml'))
        self.serialize_protocol = model.serialize_protocol
        for cls in model.classes:
            self.current_class = cls
            self.create_serialization_function(cls, SERIALIZATION, 'xml')
            self.create_serialization_function(cls, DESERIALIZATION, 'xml')

        model.parser.load_default_serialize_protocol(self.get_protocol('json'))
        self.serialize_protocol = model.serialize_protocol
        for cls in model.classes:
            self.current_class = cls
            self.create_serialization_function(cls, SERIALIZATION, 'json')
            self.create_serialization_function(cls, DESERIALIZATION, 'json')

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
        if cls.superclasses:
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
        method.body = body
        cls.functions.append(method)
        return method

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    def get_protocol(self, serialize_format):
        assert(False and "override me")

    def get_parent_serialize_format(self):
        assert(False and "override me")

    def get_serialization_function_args(self, serialize_type, serialize_format):
        assert (False and "override me")

    def build_serialize_operation(self, obj, serialization_type, serialize_format):
        assert (False and "override me")

    # pylint: enable=no-self-use
    # pylint: enable=unused-argument
