from ..base.generator_data_storage_base import GeneratorDataStorageBase


class GeneratorDataStorage(GeneratorDataStorageBase):

    def __init__(self):
        GeneratorDataStorageBase.__init__(self)

    def get_shared_method_body(self):
        return '''
if(!DataStorage.__instance)
{
    DataStorage.__instance = new DataStorage();
}
return DataStorage.__instance;'''

    def get_pattern_getter(self):
        return '''
if (name in this.{map})
{{
    return this.{map}[name];
}}
return null;'''

    def get_initialize_function_json_body(self):
        return '''let json = JSON.parse(content);
            this.deserialize_json(json);
            this._loaded = true;'''
