from ..base.GeneratorDataStorageBase import *
from ..core.Object import *
from ..core.Function import Function


class GeneratorDataStorage(GeneratorDataStorageBase):

    def __init__(self):
        GeneratorDataStorageBase.__init__(self)

    def generate(self, parser):
        GeneratorDataStorageBase.generate(self, parser)
        parser.classes.append(self)

    def create_shared_method(self):
        obj = Object()
        obj.type = self.name
        obj.name = '__instance'
        obj.is_static = True
        obj.is_pointer = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

        method = Function()
        method.name = 'shared'
        method.return_type = self.name
        method.is_static = True
        method.translated = True
        method.operations.append('        if not {}.__instance:'.format(self.name))
        method.operations.append('    {0}.__instance = {0}()'.format(self.name))
        method.operations.append('return {}.__instance'.format(self.name))
        self.functions.append(method)

    def create_getters(self, classes):
        for class_ in classes:
            if class_.is_storage and (class_.side == self.parser.side or class_.side == 'both'):
                map_name = get_data_list_name(get_data_name(class_.name))
                method = Function()
                method.name = 'get' + class_.name
                method.args.append(['name', ''])
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
        method.return_type = 'void'
        method.is_const = True
        method.args.append(['content', 'string'])
        method.translated = True

        method.operations.append('        js = json.loads(content)')
        method.operations.append('self.deserialize_json(js)')
        method.operations.append('self._loaded = True')
        self.functions.append(method)

    def add_initialize_function_xml(self):
        method = Function()
        method.name = 'initialize_xml'
        method.return_type = 'void'
        method.is_const = True
        method.args.append(['content', 'string'])
        method.translated = True

        method.operations.append('        root = ET.fromstring(content)')
        method.operations.append('self.deserialize_xml(root)')
        method.operations.append('self._loaded = True')
        self.functions.append(method)
