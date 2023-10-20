from mlc_tools.base.model import Model, SerializeFormat
from mlc_tools.core.function import Function
from mlc_tools.core.object import Objects
from ..base.generator_data_storage_base import GeneratorDataStorageBase


class GeneratorDataStorage(GeneratorDataStorageBase):

    def __init__(self):
        GeneratorDataStorageBase.__init__(self)

    def get_shared_method_body(self):
        return '''        if not DataStorage.__instance:
    DataStorage.__instance = DataStorage()
return DataStorage.__instance'''

    def get_pattern_getter(self):
        return '''        if name == '':
            return None
        if not self._loaded and name not in self.{map}:
            from .{type} import {type}
            self.{map}[name] = {type}()
            self.{map}[name].name = name
        from .DataWrapper import DataWrapper
        return DataWrapper(self.{map}[name] if name in self.{map} else None)'''

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

    def generate(self, model: Model):
        GeneratorDataStorageBase.generate(self, model)
        if model.serialize_formats & SerializeFormat.xml:
            self.add_deserialize_xml(model)
        if model.serialize_formats & SerializeFormat.json:
            self.add_deserialize_json(model)

    def add_deserialize_json(self, model):
        method = self.add_deserialize_method('deserialize_json')
        for key, obj in self.data_members.items():
            getter = 'get' + key
            map_name = obj.name
            method.operations.append(f"{map_name} = deserializer.json.get('{map_name}', None)")
            method.operations.append(f"if {map_name}:")
            method.operations.append(f"    for o in {map_name}:")
            method.operations.append(f"        self.{getter}(o['key'])")
            method.operations.append(f"    for o in {map_name}:")
            method.operations.append(f"        data = self.{getter}(o['key'])")
            method.operations.append(f"        data.deserialize_json(DeserializerJson(o['value']))")

    def add_deserialize_xml(self, model):
        method = self.add_deserialize_method('deserialize_xml')
        for key, obj in self.data_members.items():
            getter = 'get' + key
            map_name = obj.name
            method.operations.append(f"{map_name} = deserializer.node.find('{map_name}')")
            method.operations.append(f"if {map_name}:")
            method.operations.append(f"    for o in {map_name}:")
            method.operations.append(f"        self.{getter}(o.attrib['key'])")
            method.operations.append(f"    for o in {map_name}:")
            method.operations.append(f"        data = self.{getter}(o.attrib['key'])")
            method.operations.append(f"        if data:")
            method.operations.append(f"            deserializer_data = DeserializerXml(o.find('value'))")
            method.operations.append(f"            data.deserialize_xml(deserializer_data)")

    def add_deserialize_method(self, name):
        method = Function()
        method.name = name
        method.translated = True
        method.return_type = Objects.VOID
        method.is_virtual = False
        method.is_const = False
        method.operations.append('        pass')
        method.args.append(['deserializer', self])
        self.functions.append(method)
        return method


