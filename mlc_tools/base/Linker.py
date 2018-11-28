from ..core.Class import Class
from ..core.Object import *
from ..core.Function import Function
from copy import deepcopy


class Linker:

    def __init__(self):
        pass

    def link(self, model):
        self.add_functions_to_classes(model)
        self.add_members_to_classes(model)
        self.convert_superclasses(model)
        self.convert_templates(model)
        self.generate_inline_classes(model)
        self.add_get_type_method(model)
        for cls in model.classes:
            cls.on_linked(model)

    @staticmethod
    def add_get_type_method(model):
        for cls in model.classes:
            if cls.type == 'class' and cls.auto_generated:
                Linker.add_get_type_function(cls)

    @staticmethod
    def generate_inline_classes(model):
        for cls in model.classes:
            Linker._generate_inline_classes(model, cls)

    @staticmethod
    def _generate_inline_classes(model, cls):
        if len(cls.superclasses) == 0:
            return
        for superclass in cls.superclasses:
            assert (isinstance(superclass, Class))
            if superclass.__class__ != Class:
                Error.exit(Error.INTERNAL_ERROR)

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
    def convert_templates(model):
        for cls in model.classes:
            for member in cls.members:
                Linker._convert_templates(model, member)

    @staticmethod
    def _convert_templates(model, member):
        args = []
        for arg in member.template_args:
            if arg.__class__ == Object:
                args.append(arg)
            else:
                args.append(Linker.get_object_type(model, arg))
                if args[-1].__class__ == Object:
                    Linker._convert_templates(model, args[-1])
        member.template_args = args

    @staticmethod
    def get_object_type(model, type_name):
        cls = model.get_class(type_name)
        obj = Object()
        if cls is None:
            obj.type = obj.find_modifiers(type_name)
            obj.parse_type()
        else:
            obj.type = cls.name
        obj.name = ""
        return obj

    @staticmethod
    def convert_superclasses(model):
        for cls in model.classes:
            superclasses = []
            for name in cls.superclasses:
                c = model.get_class(name)
                if c is None:
                    Error.exit(Error.UNKNOWN_SUPERCLASS, cls.name, name)
                superclasses.append(c)
                c.subclasses.append(cls)
            cls.superclasses = superclasses

    @staticmethod
    def add_members_to_classes(model):
        for object_ in model.objects:
            parts = object_.name.split('::')
            if len(parts) == 2:
                class_name = parts[0]
                object_name = parts[1]
                class_ = model.get_class(class_name)
                if class_ is None:
                    Error.exit(Error.CANNOT_FIND_CLASS_FOR_OBJECT, class_name, object_.name)
                object_.name = object_name
                class_.members.append(object_)
                model.objects.remove(object_)

    @staticmethod
    def add_functions_to_classes(model):
        for method in model.functions:
            parts = method.name.split('::')
            if len(parts) == 2:
                class_name = parts[0]
                function_name = parts[1]
                class_ = model.get_class(class_name)
                if class_ is None:
                    Error.exit(Error.CANNOT_FIND_CLASS_FOR_METHOD, class_name, method.name)
                method.name = function_name
                class_.functions.append(method)
        model.functions = []

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
        method.return_type = Objects.STRING
        method.is_const = True
        method.operations.append('return {}::TYPE;'.format(cls.name))
        cls.functions.append(method)
        method.is_virtual = cls.is_virtual or len(cls.superclasses) or len(cls.subclasses)
