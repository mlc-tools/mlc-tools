from ..base.generator_data_storage_base import GeneratorDataStorageBase


class GeneratorDataStorage(GeneratorDataStorageBase):

    def __init__(self):
        GeneratorDataStorageBase.__init__(self)

    def get_shared_method_body(self):
        return '''        if not DataStorage.__instance:
    DataStorage.__instance = DataStorage()
return DataStorage.__instance'''

    def get_pattern_getter(self):
        return '''        if not self._loaded and name not in self.{map}:
            from .{type} import {type}
            self.{map}[name] = {type}()
            self.{map}[name].name = name
        from .DataWrapper import DataWrapper
        return DataWrapper(self.{map}[name])'''

    def get_initialize_function_json_body(self):
        return '''        js = json.loads(content)
        deserializer = DeserializerJson(js)
        self.deserialize_json(deserializer)
        self._loaded = True'''

    def get_initialize_function_xml_body(self):
        return '''        root = ET.fromstring(content)
        deserializer = DeserializerXml(root)
        self.deserialize_xml(deserializer)
        self._loaded = True
        '''
