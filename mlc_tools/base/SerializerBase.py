from ..core.Function import Function
from ..core.Object import Objects

SERIALIZATION = 0
DESERIALIZATION = 1


class SerializerBase:

    def __init__(self):
        self.serialize_protocol = {}
        self.parser = None
        self.current_class = None

    def generate_methods(self, parser):
        self.parser = parser
        parser.load_default_serialize_protocol(self.get_protocol('xml'))
        self.serialize_protocol = parser.serialize_protocol
        for cls in parser.classes:
            self.current_class = cls
            self.create_serialization_function(cls, SERIALIZATION, 'xml')
            self.create_serialization_function(cls, DESERIALIZATION, 'xml')

        parser.load_default_serialize_protocol(self.get_protocol('json'))
        self.serialize_protocol = parser.serialize_protocol
        for cls in parser.classes:
            self.current_class = cls
            self.create_serialization_function(cls, SERIALIZATION, 'json')
            self.create_serialization_function(cls, DESERIALIZATION, 'json')

    def create_serialization_function(self, cls, serialize_type, serialize_format):
        method = Function()
        method.name = ('serialize_' if serialize_type == SERIALIZATION else 'deserialize_') + serialize_format
        method.translated = True
        method.return_type = Objects.VOID
        for func in cls.functions:
            if func.name == method.name:
                return
    
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
        
    def get_protocol(self, serialize_format):
        assert(False and "override me")

    def get_parent_serialize_format(self):
        assert(False and "override me")

    def get_serialization_function_args(self, serialize_type, format_serialization):
        assert (False and "override me")

    def build_serialize_operation(self, obj, serialization_type, serialize_format):
        assert (False and "override me")
