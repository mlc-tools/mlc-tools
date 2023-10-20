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
        classes = self.get_storage_classes()
        for class_ in classes:
            impl = '''
            template<>const {type}* DataStorage::get(const std::string& name) const
            {{
                if(name.empty())
                {{
                    return nullptr;
                }}
                if(_loaded)
                {{
                    auto iter = {name}.find(name);
                    if(iter == {name}.end())
                    {{
                        std::cout << "Cannot find data with name [" << name << "] in DataStorage::{name}" << std::endl; 
                    }}
                    return iter != {name}.end() ? &iter->second : nullptr;
                }}
                return &const_cast<DataStorage*>(this)->{name}[name];
            }}
            '''
            name = get_data_list_name(get_data_name(class_.name))
            implementations += impl.format(name=name, type=class_.name)
        getter.specific_implementations = implementations

    def get_storage_classes(self):
        return [x for x in self.model.classes if x.is_storage and x.side in [self.model.side, 'both']]

    def get_initialize_function_json_body(self):
        collect_objects = ''
        classes = self.get_storage_classes()
        for class_ in classes:
            data_name = get_data_name(class_.name)
            map_name = get_data_list_name(data_name)
            collect_objects += f'''
            auto {data_name} = json["{map_name}"];
            for(auto& node : {data_name})
            {{
                auto name = node["key"].asString();
                non_const_this->{map_name}.emplace(name, {class_.name}());
            }} 
            '''
        return f'''Json::Value json;
        Json::Reader reader;
        reader.parse(content, json);
        auto non_const_this = const_cast<DataStorage*>(this);
        {collect_objects}
        DeserializerJson deserializer(json);
        non_const_this->_loaded = true;
        non_const_this->deserialize_json(deserializer);
        '''

    def get_initialize_function_xml_body(self):
        collect_objects = ''
        classes = self.get_storage_classes()
        for class_ in classes:
            data_name = get_data_name(class_.name)
            map_name = get_data_list_name(data_name)
            collect_objects += f'''
            for(auto& node : root.child("{map_name}"))
            {{
                auto name = node.attribute("key").as_string();
                non_const_this->{map_name}.emplace(name, {class_.name}());
            }}
            '''
        return f'''pugi::xml_document doc;
        doc.load_string(content.c_str());
        auto non_const_this = const_cast<DataStorage*>(this);
        if(doc.root() != nullptr)
        {{
            pugi::xml_node root = doc.root().first_child();
            {collect_objects}
            DeserializerXml deserializer(root);
            non_const_this->_loaded = true;
            non_const_this->deserialize_xml(deserializer);
        }}'''
