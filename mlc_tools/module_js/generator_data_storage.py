from ..base.generator_data_storage_base import GeneratorDataStorageBase
from ..base.generator_data_storage_base import get_data_list_name, get_data_name
from ..core.object import Objects
from ..core.function import Function


class GeneratorDataStorage(GeneratorDataStorageBase):

    def __init__(self):
        GeneratorDataStorageBase.__init__(self)

    def generate(self, model):
        GeneratorDataStorageBase.generate(self, model)
        model.add_class(self)

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

        method.operations.append('let json = JSON.parse(content);')
        method.operations.append('this.deserialize_json(json);')
        method.operations.append('this._loaded = true;')
        self.functions.append(method)


SHARED_METHOD = '''
if(!DataStorage.__instance)
{
    DataStorage.__instance = new DataStorage();
}
return DataStorage.__instance;
'''

PATTERN_GETTER = '''
if (name in this.{map})
{{
    return this.{map}[name];
}}
return null;
'''
