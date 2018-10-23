from ..Class import Class
from ..Object import Object
from ..Function import Function
from ..Object import AccessSpecifier


class GeneratorBase:
    def __init__(self):
        pass

    def generate_data_storage(self, parser):
        pass

    def generate_factory(self, parser, writer):
        pass

    def generate_init_files(self, parser, writer):
        pass


def get_data_name(name):
    # DataNameFoo -> name_foo
    if name.find('Data') == 0:
        name = name[4:]
    name_ = ''
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            name_ += '_'
        name_ += ch.lower()
    return name_


def get_class_name_from_data_name(name):
    # name_foo - > DataNameFoo
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
    # city -> cities
    # unit -> units
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
    
    
# TODO: Use one interface to generate DataStorage
# TODO: Dont add manual serialize methods
class DataStorage(Class):

    def __init__(self, name, classes, parser):
        Class.__init__(self)
        self.parser = parser

        self.name = name
        self.is_serialized = True

        string_obj = Object()
        string_obj.type = 'string'
        for class_ in classes:
            if class_.is_storage and (class_.side == parser.side or class_.side == 'both'):
                obj = Object()
                obj.type = 'map'
                obj.name = get_data_list_name(get_data_name(class_.name))
                obj.template_args.append(string_obj)
                obj.template_args.append(class_)
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
        self.create_getters(classes)

    def add_initialize_function_xml(self):
        pass

    def add_initialize_function_json(self):
        pass

    def create_shared_method(self):
        pass

    def create_getters(self, classes):
        pass


class DataStorageCpp(DataStorage):

    def __init__(self, *args):
        DataStorage.__init__(self, *args)

    def create_shared_method(self):
        function = Function()
        function.name = 'shared'
        function.args.append(['', ''])
        function.return_type = '{}&:const'.format(self.name)
        function.is_static = True
        function.operations.append('static {} instance;'.format(self.name))
        function.operations.append('return instance;')
        self.functions.append(function)

    @staticmethod
    def get_header_getter():
        function = Function()
        function.name = 'get'
        function.args.append(['name', 'string'])
        function.return_type = Object()
        function.return_type.type = 'template <class T> const T*'
        function.is_const = True
        function.is_template = True
        return function

    def get_source_getters(self, classes):
        string_obj = Object()
        string_obj.type = 'string'
        getters = []
        for class_ in classes:
            if class_.is_storage and (class_.side == self.parser.side or class_.side == 'both'):
                getter = Function()
                getter.is_template = True
                getter.is_const = True
                getter.name = 'get'
                getter.args.append(['name', 'string'])
                getter.return_type = Object()
                getter.return_type.type = 'template<>const {}*'.format(class_.name)
                name = get_data_list_name(get_data_name(class_.name))
                getter.operations.append('return _loaded ? &{0}.at(name) : &const_cast<{1}*>(this)->{0}[name];'.
                                         format(name, self.name))
                getters.append(getter)
        return getters


class DataStoragePhp(DataStorage):

    def __init__(self, *args):
        DataStorage.__init__(self, *args)

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
                function = Function()
                function.name = 'get' + class_.name
                function.args.append(['name', ''])
                function.operations.append(self.get_getter_pattern())
                function.operations[0] = function.operations[0].replace('@{array}', map_name)
                function.operations[0] = function.operations[0].replace('@{type}', class_.name)
                self.functions.append(function)

                function = Function()
                function.name = 'loadAll' + get_data_list_name(class_.name)
                function.operations.append(self.get_load_all_pattern())
                function.operations[0] = function.operations[0].replace('@{array}', map_name)
                function.operations[0] = function.operations[0].replace('@{type}', class_.name)
                self.functions.append(function)


class DataStorageCppXml(DataStorageCpp):

    def __init__(self, *args):
        DataStorageCpp.__init__(self, *args)

    def add_initialize_function_operations(self, function):
        function.operations.append('pugi::xml_document doc;')
        function.operations.append('doc.load(buffer_.c_str());')
        function.operations.append('const_cast<{}*>(this)->deserialize(doc.root().first_child());'.format(self.name))
        function.operations.append('const_cast<{}*>(this)->_loaded = doc.root() != nullptr;'.format(self.name))


class DataStorageCppJson(DataStorageCpp):

    def __init__(self, *args):
        DataStorageCpp.__init__(self, *args)

    def add_initialize_function_operations(self, function):
        function.operations.append('Json::Value json;')
        function.operations.append('Json::Reader reader;')
        function.operations.append('reader.parse(buffer_, json);')
        function.operations.append('const_cast<{}*>(this)->deserialize(json);'.format(self.name))
        function.operations.append('const_cast<{}*>(this)->_loaded = true;'.format(self.name))


class DataStoragePhpXml(DataStoragePhp):
    """docstring for DataStoragePythonXml"""

    def __init__(self, *args):
        DataStoragePhp.__init__(self, *args)

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
        function = Function()
        function.name = 'deserialize'
        function.args.append(['xml', ''])
        self.functions.append(function)

        function = Function()
        function.name = 'serialize'
        function.args.append(['xml', ''])
        self.functions.append(function)

    def add_initialize_function_operations(self, function):
        function.operations.append('$root = simplexml_load_string(buffer_);')
        function.operations.append('$this->deserialize(root);')
        function.operations.append('$this->_loaded = true;')

    def create_shared_method(self):
        function = Function()
        function.name = 'shared'
        # function.args.append(['', ''])
        function.return_type = self.name
        function.is_static = True
        function.operations.append('if({0}::$__instance == NULL)'.format(self.name))
        function.operations.append('{')
        function.operations.append('    {0}::$__instance = new {0}();'.format(self.name))
        function.operations.append('    {0}::$__xml = simplexml_load_file({0}::$PATH_TO_DATA);'.format(self.name))
        function.operations.append('}')
        function.operations.append('return {0}::$__instance;'.format(self.name))
        function.link()
        self.functions.append(function)

    def get_getter_pattern(self):
        return '''
            if (array_key_exists($name, $this->@{array}))
            {
                return $this->@{array}[$name];
            } else
            {
                $data = new @{type}();
                if(DataStorage::$__xml->@{array})
                {
                    foreach (DataStorage::$__xml->@{array}->pair as $node)
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
            if(DataStorage::$__xml->@{array})
            {
                foreach (DataStorage::$__xml->@{array}->pair as $node)
                {
                    $name = (string)$node["key"];
                    $this->@{array}[$name] = new @{type}();
                    $this->@{array}[$name]->deserialize($node->value);
                }
            }
            '''


class DataStoragePhpJson(DataStoragePhp):
    """docstring for DataStoragePythonXml"""

    def __init__(self, *args):
        DataStoragePhp.__init__(self, *args)

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
        function = Function()
        function.name = 'deserialize'
        function.args.append(['json', ''])
        self.functions.append(function)

        function = Function()
        function.name = 'serialize'
        function.args.append(['json', ''])
        self.functions.append(function)

    def add_initialize_function_operations(self, function):
        function.operations.append('$json = json_decode(buffer_);')
        function.operations.append('$this->deserialize(json);')
        function.operations.append('$this->_loaded = true;')

    def create_shared_method(self):
        function = Function()
        function.name = 'shared'
        # function.args.append(['', ''])
        function.return_type = self.name
        function.is_static = True
        function.operations.append('if({0}::$__instance == NULL)'.format(self.name))
        function.operations.append('{')
        function.operations.append('    {0}::$__instance = new {0}();'.format(self.name))
        function.operations.append('    $string = file_get_contents(DataStorage::$PATH_TO_DATA);')
        function.operations.append('    {0}::$__json = json_decode($string);'.format(self.name))
        function.operations.append('}')
        function.operations.append('return {0}::$__instance;'.format(self.name))
        function.link()
        self.functions.append(function)

    def get_getter_pattern(self):
        return '''
            if (array_key_exists($name, $this->@{array}))
            {
                return $this->@{array}[$name];
            } else
            {
                $data = new @{type}();
                if(DataStorage::$__json->@{array})
                {
                    foreach (DataStorage::$__json->@{array} as $node)
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
            if(DataStorage::$__json->@{array})
            {
                foreach (DataStorage::$__json->@{array} as $node)
                {
                    $name = (string)$node->key;
                    $this->@{array}[$name] = new @{type}();
                    $this->@{array}[$name]->deserialize($node->value);
                }
            }
            '''
