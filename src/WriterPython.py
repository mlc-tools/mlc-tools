from Writer import Writer
from Function import Function
from Class import Class

SERIALIZATION = 0
DESERIALIZATION = 1


def convertInitializeValue(value):
    if value == 'true':
        return 'True'
    if value == 'false':
        return 'False'
    return value


class WriterPython(Writer):

    def __init__(self, parser, serialize_format):
        Writer.__init__(self, parser, serialize_format)
        self.loaded_functions = {}
        # self.load_functions(configsDirectory + 'python_external.mlc_py')
        self.current_class = None

    def save_generated_classes(self, out_directory):
        Writer.save_generated_classes(self, out_directory)
        self.createFactory()
        self.createRequestHandler()
        # self.create_data_storage()

    def write_class(self, cls, flags):
        out = ""
        pattern = self.getPatternFile()
        self.current_class = cls

        if cls.type == 'enum':
            for member in cls.members:
                if member.initial_value is not None and member.name == '_value':
                    member.initial_value = 'self.' + member.initial_value

        initialize_list = ''
        for object in cls.members:
            initialize_list += '        ' + self.write_object(object) + '\n'

        self.createSerializationFunction(cls, SERIALIZATION)
        self.createSerializationFunction(cls, DESERIALIZATION)
        functions = ''
        for function in cls.functions:
            f = self.write_function(cls, function)
            functions += f

        imports = ''
        init_behavior = ''
        name = cls.name
        if cls.behaviors:
            name += '(' + cls.behaviors[0].name + ')'
            imports += 'from {0} import {0}'.format(cls.behaviors[0].name)
            init_behavior = '        {0}.__init__(self)'.format(cls.behaviors[0].name)
        for obj in cls.members:
            if self.parser.find_class(obj.type):
                imports += '\nfrom {0} import {0}'.format(obj.type)
            elif obj.type == 'list' or obj.type == 'map':
                for arg in obj.template_args:
                    if isinstance(arg, Class):
                        imports += '\nfrom {0} import {0}'.format(arg.name)
                    elif self.parser.find_class(arg.type):
                        imports += '\nfrom {0} import {0}'.format(arg.type)

        out = pattern.format(name, initialize_list, functions, imports, init_behavior)
        # for line in out.split('\n'):
        #     if 'get_data_storage()' in line:
        #         out = 'from DataStorage import get_data_storage\n' + out
        #         break
        # for line in out.split('\n'):
        #     if 'Factory.' in line:
        #         out = 'import Factory\n' + out
        #         break
        self.current_class = None
        return {flags: out}

    def write_function(self, cls, function):
        out = ""
        key = cls.name + '.' + function.name
        if key in self.loaded_functions:
            body = self.loaded_functions[key]
            out += '    def {0}{1}\n\n'.format(function.name, body)
        return out

    def write_object(self, object):
        value = object.initial_value
        if value is None:
            type = object.type
            if type == "string":
                value = '""'
            if type == "int":
                value = "0"
            if type == "float":
                value = "0"
            if type == "uint":
                value = "0"
            if type == "bool":
                value = "False"
            if type == "list":
                value = "[]"
            if type == "map":
                value = "{}"

        out = 'self.{0} = {1}'.format(object.name, convertInitializeValue(value))
        return out

    def _getImports(self, cls):
        return ""

    def _get_filename_of_class(self, cls):
        return cls.name + ".py"

    def load_functions(self, path):
        try:
            buffer = open(path).read()
        except IOError:
            buffer = ''
            pass
        functions = buffer.split('function:')
        for func in functions:
            k = func.find('(')
            if k == -1:
                continue
            name = func[0:k]
            rawbody = func[k:].split('\n')
            body = [rawbody[0]]
            for line in rawbody[1:]:
                if line:
                    body.append('    ' + line)
            body = '\n'.join(body)
            self.loaded_functions[name] = body

    def getSerialiationFunctionArgs(self):
        if self.serialize_format == 'xml':
            return '(self, xml)'
        return '(self, dictionary)'

    def createSerializationFunction(self, cls, serialize_type):
        function = Function()
        function.name = 'serialize' if serialize_type == SERIALIZATION else 'deserialize'
        for func in cls.functions:
            if func.name == function.name:
                return

        body = self.getSerialiationFunctionArgs() + ':\n'
        if cls.behaviors:
            body += ('        {0}.{1}' + self.getSerialiationFunctionArgs() + '\n').format(cls.behaviors[0].name,
                                                                                           function.name)
        body += '        import Factory\n'
        body += '        from DataStorage import get_data_storage\n'
        for obj in cls.members:
            if obj.is_runtime:
                continue
            if obj.is_static:
                continue
            if obj.is_const and not obj.is_link:
                continue

            body += self._buildSerializeOperation(obj.name, obj.type, convertInitializeValue(obj.initial_value),
                                                  serialize_type, obj.template_args, obj.is_pointer, 'self.', obj.is_link)
        body += '        return'
        self.loaded_functions[cls.name + '.' + function.name] = body
        cls.functions.append(function)

    def getPatternSerializationMap(self):
        return self.serialize_protocol[SERIALIZATION]['map'][0]

    def getPatternDeserializationMap(self):
        return self.serialize_protocol[DESERIALIZATION]['map'][0]

    def getPatternFile(self):
        global _pattern_file
        return _pattern_file[self.serialize_format]

    def getPatternFactoryFile(self):
        global _factory
        return _factory[self.serialize_format]

    def buildMapSerialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        str = self.getPatternSerializationMap()
        _value_is_pointer = value.is_pointer
        a0 = obj_name
        a1 = self._buildSerializeOperation('key', key_type, None, SERIALIZATION, [], False, '', key.is_link)
        a2 = self._buildSerializeOperation("value", value_type, None, SERIALIZATION, [], _value_is_pointer, '', False)
        a1 = a1.split('\n')
        for index, a in enumerate(a1):
            a1[index] = '    ' + a
        a1 = '\n'.join(a1)
        a2 = a2.split('\n')
        for index, a in enumerate(a2):
            a2[index] = '    ' + a
        a2 = '\n'.join(a2)
        return str.format(a0, a1, a2, '{}', 'self.') + '\n'
        # a1 = serialize key /simple, serialized
        # a2 = serialize value /simple, serialized, pointer,

    def buildMapDeserialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        str = self.getPatternDeserializationMap()
        _value_is_pointer = value.is_pointer
        a0 = obj_name
        a1 = self._buildSerializeOperation('key', key_type, None, DESERIALIZATION, [], False, '', key.is_link)
        a2 = self._buildSerializeOperation("value", value_type, None, DESERIALIZATION, [], _value_is_pointer, '_', False)
        a1 = a1.split('\n')
        for index, a in enumerate(a1):
            a1[index] = '    ' + a
        a1 = '\n'.join(a1)
        a2 = a2.split('\n')
        for index, a in enumerate(a2):
            a2[index] = '    ' + a
        a2 = '\n'.join(a2)
        return str.format(a0, a1, a2, '{}', 'self.') + '\n'

    def _buildSerializeOperation(self, obj_name, obj_type, obj_value, serialization_type, obj_template_args,
                                 obj_is_pointer, owner='self.', is_link=False):
        index = 0
        if obj_value is None:
            index = 1

        type = obj_type
        if self.parser.find_class(type) and self.parser.find_class(type).type == 'enum':
            type = 'string'
        elif obj_type not in self.simple_types and type != "list" and type != "map":
            if is_link:
                type = 'link'
            elif obj_is_pointer:
                type = "pointer"
            else:
                type = "serialized"
        elif obj_type in self.simple_types:
            type = obj_type
        else:
            if len(obj_template_args) > 0:
                if type == "map":
                    if len(obj_template_args) != 2:
                        print "map should have 2 arguments"
                        exit - 1
                    if serialization_type == SERIALIZATION:
                        return self.buildMapSerialization(obj_name, obj_type, obj_value, obj_is_pointer,
                                                          obj_template_args)
                    if serialization_type == DESERIALIZATION:
                        return self.buildMapDeserialization(obj_name, obj_type, obj_value, obj_is_pointer,
                                                            obj_template_args)
                else:
                    arg = obj_template_args[0]
                    arg_type = arg.name if isinstance(arg, Class) else arg.type
                    if arg.is_link:
                        type = 'list<link>'
                    elif arg_type in self.simple_types:
                        type = "list<{}>".format(arg_type)
                        obj_type = arg_type
                    elif arg.is_pointer:
                        type = "pointer_list"
                    else:
                        type = "list<serialized>"
                        obj_type = arg_type

        fstr = self.serialize_protocol[serialization_type][type][index]
        str = fstr.format(obj_name, obj_type, obj_value, '{}', owner,
                          obj_template_args[0].type if len(obj_template_args) > 0 else 'unknown_arg')
        return '        ' + str + '\n'

    def save_config_file(self):
        buffer = 'MG_XML = 2\nMG_JSON = 1\n'
        buffer += 'MG_SERIALIZE_FORMAT = MG_' + self.serialize_format.upper()
        buffer += '\n'
        self.save_file('config.py', buffer)

    def createFactory(self):
        pattern = self.getPatternFactoryFile()
        line = '        if type == "{0}": return {0}.{0}()\n'
        line_import = 'import {0}\n'
        creates = ''
        imports = ''
        for cls in self.parser.classes:
            creates += line.format(cls.name)
            imports += line_import.format(cls.name)
        factory = pattern.format(imports, creates)
        self.save_file('Factory.py', factory)

    def createRequestHandler(self):
        pattern = '''
{0}

class IRequestHandler:
    def __init__(self):
        self.response = None

    def visit(self, ctx):
        if ctx == None:
            return
{1}
{2}
'''
        line = '        elif ctx.__class__ == {0}: self.visit_{1}(ctx)\n'
        line_import = 'from {0} import {0}\n'
        line_visit = '''
    def visit_{0}(self, ctx):
        pass
'''
        lines = ''
        visits = ''
        imports = ''
        for cls in self.parser.classes:
            if self.parser.is_visitor(cls):
                func_name = cls.name
                func_name = func_name[0].lower() + func_name[1:]

                lines += line.format(cls.name, func_name)
                imports += line_import.format(cls.name)
                visits += line_visit.format(func_name)
        factory = pattern.format(imports, lines, visits)
        self.save_file('IRequestHandler.py', factory)

    def create_data_storage(self):
        pattern = '''
class DataStorage():
    def getDataBuilding(self, name):
        import DataBuilding
        data = DataBuilding.DataBuilding()
        data.name = name
        return data
    def getDataResource(self, name):
        import DataResource
        data = DataResource.DataResource()
        data.name = name
        return data
    def getDataLocale(self, name):
        import DataLocale
        data = DataLocale.DataLocale()
        data.name = name
        return data

def get_data_storage():
    return DataStorage()
'''
        self.save_file('DataStorage.py', pattern)


_factory = {}
_factory['xml'] = '''import xml.etree.ElementTree as ET
{0}
class Factory:
    @staticmethod
    def build(type):
{1}
        return None
    @staticmethod
    def create_command(string):
        root = ET.fromstring(string)
        type = root.tag
        command = Factory.build(type)
        if command != None:
            command.deserialize(root)
        return command'''

_factory['json'] = '''import json
{0}
class Factory:
    @staticmethod
    def build(type):
{1}
        return None
    @staticmethod
    def create_command(string):
        dictionary = json.loads(string)
        type = dictionary["command"]["type"]
        command = Factory.build(type)
        if command != None:
            command.deserialize(dictionary)
        return command'''

_pattern_file = {}
_pattern_file['xml'] = '''import xml.etree.ElementTree as ET
{3}\nclass {0}:
    def __init__(self):\n{4}\n{1}\n        pass
    def get_type(self):\n        return self.__type__
{2}'''

_pattern_file['json'] = '''import json
{3}
class {0}:
    def __init__(self):\n{4}\n{1}\n        pass
    def get_type(self):\n        return self.__type__
{2}'''
