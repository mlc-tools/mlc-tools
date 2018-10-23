from ..language.Generator_ import *
from ..Object import *
from ..Function import Function


class Generator(GeneratorBase):
    def __init__(self):
        GeneratorBase.__init__(self)

    def generate_data_storage(self, parser):
        storage = DataStoragePython('DataStorage', parser.classes, parser)
        parser.classes.append(storage)

    def generate_factory(self, parser, writer):
        from .constants import FACTORY
        
        line = '''
        if type == "{0}":
            from . import {0}
            return {0}.{0}()'''
        builders = ''
        for cls in parser.classes:
            builders += line.format(cls.name)
        content = FACTORY.format(builders=builders)
        writer.save_file('Factory.py', content)

    def generate_init_files(self, parser, writer):
        writer.save_file('__init__.py', '')


class DataStoragePython(DataStorage):

    def __init__(self, *args):
        DataStorage.__init__(self, *args)

    def create_shared_method(self):
        obj = Object()
        obj.type = self.name
        obj.name = '__instance'
        obj.is_static = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

        method = Function()
        method.name = 'shared'
        method.args.append(['', ''])
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
        method.operations.append('self.deserialize(js)')
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
        method.operations.append('self.deserialize(root)')
        method.operations.append('self._loaded = True')
        self.functions.append(method)
