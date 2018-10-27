from ..core.Class import Class
from ..core.Object import *
from ..core.Function import Function
from copy import deepcopy


class Linker:

    def __init__(self):
        pass

    def link(self, parser):
        self.add_functions_to_classes(parser)
        self.add_members_to_classes(parser)
        self.convert_superclasses(parser)
        self.convert_templates(parser)
        self.generate_inline_classes(parser)
        self.add_get_type_method(parser)
        self.link_functions(parser)
        for cls in parser.classes:
            cls.on_linked(parser)

    @staticmethod
    def add_get_type_method(parser):
        for cls in parser.classes:
            if cls.type == 'class' and cls.auto_generated:
                Linker.add_get_type_function(cls)

    @staticmethod
    def generate_inline_classes(parser):
        for cls in parser.classes:
            Linker._generate_inline_classes(parser, cls)

    @staticmethod
    def _generate_inline_classes(parser, cls):
        if len(cls.superclasses) == 0:
            return
        for superclass in cls.superclasses:
            if not isinstance(superclass, Class):
                Error.exit(Error.INTERNAL_ERROR)
                Linker._generate_inline_classes(parser, superclass)
            if not superclass.is_inline:
                continue
            for obj in superclass.members:
                copy = deepcopy(obj)
                cls.members.append(copy)
            for func in superclass.functions:
                disallow = False
                disallow = disallow or func.name == 'operator =='
                disallow = disallow or func.name == 'operator !='
                if disallow:
                    continue
                copy = deepcopy(func)
                cls.functions.append(copy)

            superclass.subclasses.remove(cls)

        cls.superclasses = [i for i in cls.superclasses if not i.is_inline]

    @staticmethod
    def link_functions(parser):
        for cls in parser.classes:
            for func in cls.functions:
                func.link()

    @staticmethod
    def convert_templates(parser):
        for cls in parser.classes:
            for member in cls.members:
                Linker._convert_templates(parser, member)

    @staticmethod
    def _convert_templates(parser, member):
        args = []
        for arg in member.template_args:
            if isinstance(arg, Object):
                args.append(arg)
            else:
                args.append(Linker.get_object_type(parser, arg))
                if isinstance(args[-1], Object):
                    Linker._convert_templates(parser, args[-1])
        member.template_args = args

    @staticmethod
    def get_object_type(parser, type_name):
        cls = parser.find_class(type_name)
        obj = Object()
        if cls is None:
            obj.type = obj.find_modifiers(type_name)
            obj.parse_type()
        else:
            obj.type = cls
        obj.name = ""
        return obj

    @staticmethod
    def convert_superclasses(parser):
        for cls in parser.classes:
            superclasses = []
            for name in cls.superclasses:
                c = parser.find_class(name)
                if c is None:
                    Error.exit(Error.UNKNOWN_SUPERCLASS, cls.name, name)
                superclasses.append(c)
                c.subclasses.append(cls)
            cls.superclasses = superclasses

    @staticmethod
    def add_members_to_classes(parser):
        for object_ in parser.objects:
            parts = object_.name.split('::')
            if len(parts) == 2:
                class_name = parts[0]
                object_name = parts[1]
                class_ = parser.find_class(class_name)
                if class_ is None:
                    Error.exit(Error.CANNOT_FIND_CLASS_FOR_OBJECT, class_name, object_.name)
                object_.name = object_name
                class_.members.append(object_)
                parser.objects.remove(object_)

    @staticmethod
    def add_functions_to_classes(parser):
        for method in parser.functions:
            parts = method.name.split('::')
            if len(parts) == 2:
                class_name = parts[0]
                function_name = parts[1]
                class_ = parser.find_class(class_name)
                if class_ is None:
                    Error.exit(Error.CANNOT_FIND_CLASS_FOR_METHOD, class_name, method.name)
                method.name = function_name
                class_.functions.append(method)
        parser.functions = []

    @staticmethod
    def add_get_type_function(cls):
        member = Object()
        member.is_static = True
        member.is_const = True
        member.type = 'string'
        member.name = 'TYPE'
        member.initial_value = '"{}"'.format(cls.name)
        member.access = AccessSpecifier.public
        cls.members.append(member)

        method = Function()
        method.name = 'get_type'
        method.return_type = 'string'
        method.is_const = True
        method.operations.append('return {}::TYPE;'.format(cls.name))
        cls.functions.append(method)
        method.is_virtual = cls.is_virtual or len(cls.superclasses) or len(cls.subclasses)
