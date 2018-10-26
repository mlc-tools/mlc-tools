from ..base.GeneratorDataStorageBase import *
from ..core.Object import *
from ..core.Function import Function


class GeneratorDataStorage(GeneratorDataStorageBase):

    def __init__(self):
        GeneratorDataStorageBase.__init__(self)

    def generate(self, parser):
        GeneratorDataStorageBase.generate(self, parser)
        parser.classes.append(self)

    def create_shared_method(self):
        method = Function()
        method.name = 'shared'
        method.return_type = '{}&:const'.format(self.name)
        method.is_static = True
        method.operations.append('static {} instance;'.format(self.name))
        method.operations.append('return instance;')
        self.functions.append(method)

    def create_getters(self, classes):
        method = Function()
        method.name = 'get'
        method.args.append(['name', 'string'])
        method.return_type = Object()
        method.return_type.type = 'template <class T> const T*'
        method.is_const = True
        method.is_template = True
        return method

    def get_source_getters(self, classes):
        string_obj = Object()
        string_obj.type = 'string'
        getters = []
        for class_ in classes:
            if class_.is_storage and (class_.side == self.parser.side or class_.side == 'both'):
                getter = Function()
                getter.is_template = True
                getter.is_const = True
                getter.name = 'get'
                getter.args.append(['name', 'string'])
                getter.return_type = Object()
                getter.return_type.type = 'template<>const {}*'.format(class_.name)
                name = get_data_list_name(get_data_name(class_.name))
                getter.operations.append('return _loaded ? &{0}.at(name) : &const_cast<{1}*>(this)->{0}[name];'.
                                         format(name, self.name))
                getters.append(getter)
        return getters

    def add_initialize_function_json(self):
        method = Function()
        method.name = 'initialize_json'
        method.return_type = 'void'
        method.is_const = True
        method.args.append(['content', 'string'])
        method.translated = True

        method.operations.append('Json::Value json;')
        method.operations.append('Json::Reader reader;')
        method.operations.append('reader.parse(buffer_, json);')
        method.operations.append('const_cast<{}*>(this)->deserialize(json);'.format(self.name))
        method.operations.append('const_cast<{}*>(this)->_loaded = true;'.format(self.name))
        self.functions.append(method)

    def add_initialize_function_xml(self):
        method = Function()
        method.name = 'initialize_xml'
        method.return_type = 'void'
        method.is_const = True
        method.args.append(['content', 'string'])
        method.translated = True

        method.operations.append('pugi::xml_document doc;')
        method.operations.append('doc.load(buffer_.c_str());')
        method.operations.append('const_cast<{}*>(this)->deserialize(doc.root().first_child());'.format(self.name))
        method.operations.append('const_cast<{}*>(this)->_loaded = doc.root() != nullptr;'.format(self.name))
        self.functions.append(method)
