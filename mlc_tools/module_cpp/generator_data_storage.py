from ..base import Parser
from ..base.generator_data_storage_base import GeneratorDataStorageBase
from ..base.generator_data_storage_base import get_data_list_name, get_data_name
from ..core.object import Object, Objects
from ..core.function import Function


class GeneratorDataStorage(GeneratorDataStorageBase):

    def __init__(self):
        GeneratorDataStorageBase.__init__(self)

    def generate(self, model):
        GeneratorDataStorageBase.generate(self, model)
        model.add_class(self)

    def create_shared_method(self):
        method = Function()
        method.name = 'shared'
        method.return_type = Parser.create_object('{}&:const'.format(self.name))
        method.is_static = True
        method.operations.append('static {} instance;'.format(self.name))
        method.operations.append('return instance;')
        self.functions.append(method)

    def create_getters(self, classes):
        method = Function()
        method.name = 'get'
        method.args.append(['name', Objects.STRING])
        method.return_type = Object()
        method.return_type.type = 'template <class T> const T*'
        method.is_const = True
        method.is_template = True
        self.functions.append(method)
        self.generate_implementations(classes, method)
        return method

    def generate_implementations(self, classes, getter):
        implementations = ''
        for class_ in classes:
            if class_.is_storage and (class_.side == self.model.side or class_.side == 'both'):
                impl = '''
                template<>const {type}* DataStorage::get(const std::string& name) const
                {{
                    return _loaded ? &{name}.at(name) : &const_cast<DataStorage*>(this)->{name}[name];
                }}
                '''
                name = get_data_list_name(get_data_name(class_.name))
                implementations += impl.format(name=name, type=class_.name)
        getter.specific_implementations = implementations

    def add_initialize_function_json(self):
        method = Function()
        method.name = 'initialize_json'
        method.return_type = Objects.VOID
        method.is_const = True
        method.args.append(['content', Objects.STRING])
        method.translated = True

        method.operations.append('Json::Value json;')
        method.operations.append('Json::Reader reader;')
        method.operations.append('reader.parse(content, json);')
        method.operations.append('const_cast<{}*>(this)->deserialize_json(json);'.format(self.name))
        method.operations.append('const_cast<{}*>(this)->_loaded = true;'.format(self.name))
        self.functions.append(method)

    def add_initialize_function_xml(self):
        method = Function()
        method.name = 'initialize_xml'
        method.return_type = Objects.VOID
        method.is_const = True
        method.args.append(['content', Objects.STRING])
        method.translated = True

        method.operations.append('pugi::xml_document doc;')
        method.operations.append('doc.load(content.c_str());')
        method.operations.append('const_cast<{}*>(this)->deserialize_xml(doc.root().first_child());'.format(self.name))
        method.operations.append('const_cast<{}*>(this)->_loaded = doc.root() != nullptr;'.format(self.name))
        self.functions.append(method)
