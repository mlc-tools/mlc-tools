from ..core.class_ import Class
from ..core.object import Object, Objects
from ..core.object import AccessSpecifier
from ..core.function import Function
from ..base.parser import Parser
from ..base.model import SerializeFormat


def get_data_name(name):
    """
    convert DataNameFoo -> name_foo
    :param name: name of class in uppercase
    :return: name in lowercase
    """
    if name.find('Data') == 0:
        name = name[4:]
    name_ = ''
    for i, char in enumerate(name):
        if char.isupper() and i > 0:
            name_ += '_'
        name_ += char.lower()
    return name_


def get_class_name_from_data_name(name):
    """
    convert name_foo - > DataNameFoo
    :param name: name in lowercase
    :return: name of class in uppercase
    """
    upper = True
    name_ = ''
    for char in name:
        if char == '_':
            upper = True
            continue
        name_ += char if not upper else char.upper()
        upper = False
    return 'Data' + name_


def get_data_list_name(name):
    """ get plural form
    city -> cities
    unit -> units
    :param str name: name of unit
    :return:
    """
    last = name[-1]
    if last in 'y':
        if last in 'a,e,i,o,u,y':
            name = name[0:-1] + 'ies'
        else:
            name += 's'
    elif last in 'ou':
        name += 'es'
    elif last == 'f':
        name = name[0:-1] + 'ves'
    elif name[-2:-1] == 'fe':
        name = name[0:-2] + 'ves'
    elif last in ['s', 'ss', 'x', 'sh', 'ch']:
        name += 'es'
    else:
        name += 's'
    return name


# TODO: Use one interface to generate GeneratorDataStorageBase
# TODO: Dont add manual serialize methods
class GeneratorDataStorageBase(Class):

    def __init__(self):
        Class.__init__(self)
        self.model = None

    def generate(self, model):
        self.model = model

        self.name = 'DataStorage'
        self.is_serialized = True

        for class_ in model.classes:
            if class_.is_storage and (class_.side == model.side or class_.side == 'both'):
                obj = Object()
                obj.type = 'map'
                obj.name = get_data_list_name(get_data_name(class_.name))
                obj.template_args.append(Objects.STRING)
                obj.template_args.append(class_.name)

                obj.access = AccessSpecifier.public
                self.members.append(obj)

        loaded = Object()
        loaded.is_runtime = True
        loaded.name = '_loaded'
        loaded.type = 'bool'
        loaded.initial_value = 'false'
        loaded.access = AccessSpecifier.private
        self.members.append(loaded)

        self.create_shared_method()
        if model.serialize_formats & SerializeFormat.xml:
            self.add_initialize_function_xml()
        if model.serialize_formats & SerializeFormat.json:
            self.add_initialize_function_json()
        self.create_getters(model.classes)

    def add_initialize_function_xml(self):
        pass

    def add_initialize_function_json(self):
        pass

    def create_shared_method(self):
        obj = Object()
        obj.type = self.name
        obj.name = '__instance'
        obj.is_static = True
        obj.is_pointer = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

        method = Function()
        method.name = 'shared'
        method.return_type = Parser.create_object(self.name)
        method.is_static = True
        method.translated = True
        method.operations.extend(self.get_shared_method_body().split('\n'))
        self.functions.append(method)

    def get_shared_method_body(self):
        assert False and 'Override me'

    def create_getters(self, classes):
        pass
