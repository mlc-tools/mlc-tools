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
        return self.{map}[name]'''

    def get_initialize_function_json_body(self):
        return '''        js = json.loads(content)
        self.deserialize_json(js)
        self._loaded = True'''

    def get_initialize_function_xml_body(self):
        return '''        root = ET.fromstring(content)
        self.deserialize_xml(root)
        self._loaded = True
        '''