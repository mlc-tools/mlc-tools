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
                method.operations.append('        if not self._loaded and name not in self.{}:'.format(map_name))
                method.operations.append('    from .{0} import {0}'.format(class_.name))
                method.operations.append('    self.{}[name] = {}()'.format(map_name, class_.name))
                method.operations.append('    self.{}[name].name = name'.format(map_name))
                method.operations.append('return self.{}[name]'.format(map_name))
                method.translated = True
                self.functions.append(method)

    def add_initialize_function_json(self):
        method = Function()
        method.name = 'initialize_json'
        method.return_type = Objects.VOID
        method.is_const = True
        method.args.append(['content', Objects.STRING])
        method.translated = True

        method.operations.append('        js = json.loads(content)')
        method.operations.append('self.deserialize_json(js)')
        method.operations.append('self._loaded = True')
        self.functions.append(method)

    def add_initialize_function_xml(self):
        method = Function()
        method.name = 'initialize_xml'
        method.return_type = Objects.VOID
        method.is_const = True
        method.args.append(['content', Objects.STRING])
        method.translated = True

        method.operations.append('        root = ET.fromstring(content)')
        method.operations.append('self.deserialize_xml(root)')
        method.operations.append('self._loaded = True')
        self.functions.append(method)


SHARED_METHOD = '''
if not DataStorage.__instance:
    DataStorage.__instance = DataStorage()
return DataStorage.__instance
'''
