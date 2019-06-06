from ..base.generator_data_storage_base import GeneratorDataStorageBase
from ..base.generator_data_storage_base import get_data_list_name, get_data_name
from ..core.object import Object, AccessSpecifier, Objects
from ..core.function import Function


class GeneratorDataStorage(GeneratorDataStorageBase):

    def __init__(self):
        GeneratorDataStorageBase.__init__(self)

    def generate(self, model):
        GeneratorDataStorageBase.generate(self, model)
        model.add_class(self)

    def create_shared_method(self):
        GeneratorDataStorageBase.create_shared_method(self)

        obj = Object()
        obj.type = self.name
        obj.name = '__xml'
        obj.initial_value = 'null'
        obj.is_static = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

        obj = Object()
        obj.type = Objects.STRING
        obj.name = 'PATH_TO_DATA'
        obj.initial_value = '"assets/data/data.xml"'
        obj.is_static = True
        self.members.append(obj)

        obj = Object()
        obj.type = self.name
        obj.name = '__json'
        obj.initial_value = 'null'
        obj.is_static = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

        # method = Function()
        # method.name = 'deserialize_xml'
        # method.args.append(['xml', Objects.VOID])
        # self.functions.append(method)
        # method = Function()
        # method.name = 'deserialize_json'
        # method.args.append(['xml', Objects.VOID])
        # self.functions.append(method)

        # method = Function()
        # method.name = 'serialize_xml'
        # method.args.append(['xml', Objects.VOID])
        # self.functions.append(method)
        # method = Function()
        # method.name = 'serialize_json'
        # method.args.append(['xml', Objects.VOID])
        # self.functions.append(method)

    def get_shared_method_body(self):
        return SHARED_METHOD

    def create_getters(self, classes):
        for class_ in classes:
            if class_.is_storage and (class_.side == self.model.side or class_.side == 'both'):
                map_name = get_data_list_name(get_data_name(class_.name))
                method = Function()
                method.name = 'get' + class_.name
                method.args.append(['name', Objects.VOID])

                body = PATTERN_GETTER.format(map=map_name, type=class_.name)
                method.operations.append(body)
                method.translated = True
                self.functions.append(method)

    def add_initialize_function_json(self):
        method = Function()
        method.name = 'initialize_json'
        method.return_type = Objects.VOID
        method.is_const = True
        method.args.append(['content', Objects.STRING])
        method.translated = True

        method.operations.append('DataStorage.__json = JSON.parse(content);')
        method.operations.append('this.deserialize_json(DataStorage.__json);')
        method.operations.append('this._loaded = true;')
        self.functions.append(method)

    def add_initialize_function_xml(self):
        # method = Function()
        # method.name = 'initialize_xml'
        # method.return_type = Objects.VOID
        # method.is_const = True
        # method.args.append(['content', Objects.STRING])
        # method.translated = True

        # method.operations.append('root = simplexml_load_string(content);')
        # method.operations.append('this.deserialize_xml(root);')
        # method.operations.append('this._loaded = true;')
        # self.functions.append(method)
        pass


SHARED_METHOD = '''
if(!DataStorage.__instance)
{
    DataStorage.__instance = new DataStorage();
    //DataStorage.__json = JSON.parse(string);
}
return DataStorage.__instance;
'''

PATTERN_GETTER = '''
//TODO:
'''

PATTERN_LOAD_ALL = '''
//TODO:
'''


PATTERN_GETTER = '''
if (name in this.{map})
{{
    return this.{map}[name];
}}
else if (DataStorage.__json != null)
{{
    let data = new {type}();
    for (let index in DataStorage.__json.units)
    {{
        let node = DataStorage.__json.units[index];
        if (node.key == name)
        {{
            this.{map}[name] = data;
            data.deserialize_json(node.value);
        }}
    }}
    return this.{map}[name];
}}
'''
