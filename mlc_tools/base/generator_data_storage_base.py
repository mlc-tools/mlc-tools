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


class GeneratorDataStorageBase(Class):

    def __init__(self):
        Class.__init__(self)
        self.model = None
        self.data_members = {}

    def generate(self, model):
        self.model = model

        self.name = 'DataStorage'
        self.is_serialized = True

        for class_ in model.classes:
            if class_.is_storage and (class_.side in [model.side, 'both']):
                obj = Object()
                obj.type = 'map'
                obj.name = get_data_list_name(get_data_name(class_.name))
                obj.template_args.append(Objects.STRING)
                obj.template_args.append(class_.name)
                obj.access = AccessSpecifier.private
                self.members.append(obj)
                self.data_members[class_.name] = obj

                self.create_keys_getter(obj.name)

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
        self.create_getters_maps(model.classes)
        model.add_class(self)

    def add_initialize_function_xml(self):
        method = Function()
        method.name = 'initialize_xml'
        method.return_type = Objects.VOID
        method.is_const = True
        method.args.append(['content', Objects.STRING])
        method.translated = True
        method.operations.append(self.get_initialize_function_xml_body())
        self.functions.append(method)

    def add_initialize_function_json(self):
        method = Function()
        method.name = 'initialize_json'
        method.return_type = Objects.VOID
        method.is_const = True
        method.args.append(['content', Objects.STRING])
        method.translated = True
        method.operations.append(self.get_initialize_function_json_body())
        self.functions.append(method)

    def get_initialize_function_json_body(self):
        pass

    def get_initialize_function_xml_body(self):
        pass

    def is_need_create_static_instance(self):
        return True

    def create_shared_method(self):
        if self.is_need_create_static_instance():
            obj = Object()
            obj.type = self.name
            obj.name = '__instance'
            obj.is_static = True
            obj.is_pointer = True
            obj.access = AccessSpecifier.private
            self.members.append(obj)

        method = Function()
        method.name = 'shared'
        method.return_type = Parser.create_object('{}&:const'.format(self.name))
        method.is_static = True
        method.translated = True
        method.operations.extend(self.get_shared_method_body().split('\n'))
        self.functions.append(method)

    def get_shared_method_body(self):
        assert False and 'Override me'

    def create_getters(self, classes):
        for class_ in classes:
            if class_.is_storage and class_.side in [self.model.side, 'both']:
                map_name = get_data_list_name(get_data_name(class_.name))
                method = Function()
                method.name = 'get' + class_.name
                method.args.append(['name', Objects.VOID])

                body = self.get_pattern_getter().format(map=map_name, type=class_.name)
                method.operations.append(body)
                method.translated = True
                self.functions.append(method)

    def get_pattern_getter(self):
        return ''

    def create_keys_getter(self, map_name):
        method = Function()
        method.name = f'get_{map_name}_keys'
        method.is_const = True
        method.return_type = Parser.create_object('list<string>')
        method.operations.append(f'''
        list<std::string> result;
        for(auto&& [key, _] : this->{map_name})
        {{
            list_push(result, key);   
        }}
        return result;
        ''')
        self.functions.append(method)

    def create_getters_maps(self, classes):
        for class_ in classes:
            if class_.is_storage and class_.side in [self.model.side, 'both']:
                method = Function()
                map_name = get_data_list_name(get_data_name(class_.name))
                method.name = f'get_{map_name}'
                method.is_const = True
                method.return_type = Parser.create_object(f'map<string, {class_.name}>:const:ref')
                method.operations.append(f'''
                return this->{map_name};
                ''')
                self.functions.append(method)
