from ..base.generator_data_storage_base import GeneratorDataStorageBase
from ..base.generator_data_storage_base import get_data_list_name, get_data_name
from ..core.object import Object, Objects
from ..core.function import Function


class GeneratorDataStorage(GeneratorDataStorageBase):

    def __init__(self):
        GeneratorDataStorageBase.__init__(self)

    def is_need_create_static_instance(self):
        return False

    def get_shared_method_body(self):
        return '''static DataStorage instance;
                  return instance;'''

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
            if class_.is_storage and class_.side in [self.model.side, 'both']:
                impl = '''
                template<>const {type}* DataStorage::get(const std::string& name) const
                {{
                    return _loaded ? &{name}.at(name) : &const_cast<DataStorage*>(this)->{name}[name];
                }}
                '''
                name = get_data_list_name(get_data_name(class_.name))
                implementations += impl.format(name=name, type=class_.name)
        getter.specific_implementations = implementations

    def get_initialize_function_json_body(self):
        return '''Json::Value json;
        Json::Reader reader;
        reader.parse(content, json);
        const_cast<DataStorage*>(this)->deserialize_json(json);
        const_cast<DataStorage*>(this)->_loaded = true;'''

    def get_initialize_function_xml_body(self):
        return '''pugi::xml_document doc;
        doc.load(content.c_str());
        const_cast<DataStorage*>(this)->deserialize_xml(doc.root().first_child());
        const_cast<DataStorage*>(this)->_loaded = doc.root() != nullptr;'''
