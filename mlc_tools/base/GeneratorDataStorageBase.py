from ..core.Class import Class
from ..core.Object import Object
from ..core.Function import Function
from ..core.Object import AccessSpecifier


def get_data_name(name):
    """
    convert DataNameFoo -> name_foo
    :param name: name of class in uppercase
    :return: name in lowercase
    """
    if name.find('Data') == 0:
        name = name[4:]
    name_ = ''
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            name_ += '_'
        name_ += ch.lower()
    return name_


def get_class_name_from_data_name(name):
    """
    convert name_foo - > DataNameFoo
    :param name: name in lowercase
    :return: name of class in uppercase
    """
    upper = True
    name_ = ''
    for ch in name:
        if ch == '_':
            upper = True
            continue
        name_ += ch if not upper else ch.upper()
        upper = False
    return 'Data' + name_


def get_data_list_name(name):
    """ get plural form
    city -> cities
    unit -> units
    :param str name: name of unit
    :return:
    """
    last = name[-1]
    if last in 'y':
        if last in 'a,e,i,o,u,y':
            name = name[0:-1] + 'ies'
        else:
            name += 's'
    elif last in 'ou':
        name += 'es'
    elif last == 'f':
        name = name[0:-1] + 'ves'
    elif name[-2:-1] == 'fe':
        name = name[0:-2] + 'ves'
    elif last in ['s', 'ss', 'x', 'sh', 'ch']:
        name += 'es'
    else:
        name += 's'
    return name


# TODO: Use one interface to generate GeneratorDataStorageBase
# TODO: Dont add manual serialize methods
class GeneratorDataStorageBase(Class):

    def __init__(self):
        Class.__init__(self)
        self.parser = None

    def generate(self, parser):
        self.parser = parser

        self.name = 'DataStorage'
        self.is_serialized = True

        for class_ in parser.classes:
            if class_.is_storage and (class_.side == parser.side or class_.side == 'both'):
                obj = Object()
                obj.type = 'map'
                obj.name = get_data_list_name(get_data_name(class_.name))
                obj.template_args.append('string')
                obj.template_args.append(class_.name)
                
                obj.access = AccessSpecifier.public
                self.members.append(obj)

        loaded = Object()
        loaded.is_runtime = True
        loaded.name = '_loaded'
        loaded.type = 'bool'
        loaded.initial_value = 'false'
        loaded.access = AccessSpecifier.private
        self.members.append(loaded)

        self.create_shared_method()
        self.add_initialize_function_xml()
        self.add_initialize_function_json()
        self.create_getters(parser.classes)

    def add_initialize_function_xml(self):
        pass

    def add_initialize_function_json(self):
        pass

    def create_shared_method(self):
        pass

    def create_getters(self, classes):
        pass


class DataStoragePhp(GeneratorDataStorageBase):

    def __init__(self):
        GeneratorDataStorageBase.__init__(self)

        obj = Object()
        obj.type = self.name
        obj.name = '__instance'
        obj.initial_value = 'NULL'
        obj.is_static = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

        self.create_deserialize()

    def create_deserialize(self):
        pass

    def get_getter_pattern(self):
        pass

    def get_load_all_pattern(self):
        pass

    def create_getters(self, classes):
        for class_ in classes:
            if class_.is_storage and (class_.side == self.parser.side or class_.side == 'both'):
                map_name = get_data_list_name(get_data_name(class_.name))
                method = Function()
                method.name = 'get' + class_.name
                method.args.append(['name', ''])
                method.operations.append(self.get_getter_pattern())
                method.operations[0] = method.operations[0].replace('@{array}', map_name)
                method.operations[0] = method.operations[0].replace('@{type}', class_.name)
                self.functions.append(method)

                method = Function()
                method.name = 'loadAll' + get_data_list_name(class_.name)
                method.operations.append(self.get_load_all_pattern())
                method.operations[0] = method.operations[0].replace('@{array}', map_name)
                method.operations[0] = method.operations[0].replace('@{type}', class_.name)
                self.functions.append(method)


class DataStoragePhpXml(DataStoragePhp):
    """docstring for DataStoragePythonXml"""

    def __init__(self):
        DataStoragePhp.__init__(self)

        obj = Object()
        obj.type = self.name
        obj.name = '__xml'
        obj.initial_value = 'NULL'
        obj.is_static = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

        obj = Object()
        obj.type = 'string'
        obj.name = 'PATH_TO_DATA'
        obj.initial_value = '"assets/data/data.xml"'
        obj.is_static = True
        obj.access = AccessSpecifier.public
        self.members.append(obj)

    def create_deserialize(self):
        method = Function()
        method.name = 'deserialize'
        method.args.append(['xml', ''])
        self.functions.append(method)

        method = Function()
        method.name = 'serialize'
        method.args.append(['xml', ''])
        self.functions.append(method)

    def add_initialize_function_operations(self, method):
        method.operations.append('$root = simplexml_load_string(buffer_);')
        method.operations.append('$this->deserialize(root);')
        method.operations.append('$this->_loaded = true;')

    def create_shared_method(self):
        method = Function()
        method.name = 'shared'
        # method.args.append(['', ''])
        method.return_type = self.name
        method.is_static = True
        method.operations.append('if({0}::$__instance == NULL)'.format(self.name))
        method.operations.append('{')
        method.operations.append('    {0}::$__instance = new {0}();'.format(self.name))
        method.operations.append('    {0}::$__xml = simplexml_load_file({0}::$PATH_TO_DATA);'.format(self.name))
        method.operations.append('}')
        method.operations.append('return {0}::$__instance;'.format(self.name))
        method.link()
        self.functions.append(method)

    def get_getter_pattern(self):
        return '''
            if (array_key_exists($name, $this->@{array}))
            {
                return $this->@{array}[$name];
            } else
            {
                $data = new @{type}();
                if(GeneratorDataStorageBase::$__xml->@{array})
                {
                    foreach (GeneratorDataStorageBase::$__xml->@{array}->pair as $node)
                    {
                        if ($node["key"] == $name)
                        {
                            $this->@{array}[$name] = $data;
                            $data->deserialize($node->value);
                        }
                    }
                }
                return $data;
            }
            '''

    def get_load_all_pattern(self):
        return '''
            if(GeneratorDataStorageBase::$__xml->@{array})
            {
                foreach (GeneratorDataStorageBase::$__xml->@{array}->pair as $node)
                {
                    $name = (string)$node["key"];
                    $this->@{array}[$name] = new @{type}();
                    $this->@{array}[$name]->deserialize($node->value);
                }
            }
            '''


class DataStoragePhpJson(DataStoragePhp):
    """docstring for DataStoragePythonXml"""

    def __init__(self):
        DataStoragePhp.__init__(self)

        obj = Object()
        obj.type = self.name
        obj.name = '__json'
        obj.initial_value = 'NULL'
        obj.is_static = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

        obj = Object()
        obj.type = 'string'
        obj.name = 'PATH_TO_DATA'
        obj.initial_value = '"assets/data/data.json"'
        obj.is_static = True
        obj.access = AccessSpecifier.public
        self.members.append(obj)

    def create_deserialize(self):
        method = Function()
        method.name = 'deserialize'
        method.args.append(['json', ''])
        self.functions.append(method)

        method = Function()
        method.name = 'serialize'
        method.args.append(['json', ''])
        self.functions.append(method)

    def add_initialize_function_operations(self, method):
        method.operations.append('$json = json_decode(buffer_);')
        method.operations.append('$this->deserialize(json);')
        method.operations.append('$this->_loaded = true;')

    def create_shared_method(self):
        method = Function()
        method.name = 'shared'
        # method.args.append(['', ''])
        method.return_type = self.name
        method.is_static = True
        method.operations.append('if({0}::$__instance == NULL)'.format(self.name))
        method.operations.append('{')
        method.operations.append('    {0}::$__instance = new {0}();'.format(self.name))
        method.operations.append('    $string = file_get_contents(GeneratorDataStorageBase::$PATH_TO_DATA);')
        method.operations.append('    {0}::$__json = json_decode($string);'.format(self.name))
        method.operations.append('}')
        method.operations.append('return {0}::$__instance;'.format(self.name))
        method.link()
        self.functions.append(method)

    def get_getter_pattern(self):
        return '''
            if (array_key_exists($name, $this->@{array}))
            {
                return $this->@{array}[$name];
            } else
            {
                $data = new @{type}();
                if(GeneratorDataStorageBase::$__json->@{array})
                {
                    foreach (GeneratorDataStorageBase::$__json->@{array} as $node)
                    {
                        if ($node->key == $name)
                        {
                            $this->@{array}[$name] = $data;
                            $data->deserialize($node->value);
                        }
                    }
                }
                return $data;
            }
            '''

    def get_load_all_pattern(self):
        return '''
            if(GeneratorDataStorageBase::$__json->@{array})
            {
                foreach (GeneratorDataStorageBase::$__json->@{array} as $node)
                {
                    $name = (string)$node->key;
                    $this->@{array}[$name] = new @{type}();
                    $this->@{array}[$name]->deserialize($node->value);
                }
            }
            '''
