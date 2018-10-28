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
        obj.initial_value = 'NULL'
        obj.is_static = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

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

        obj = Object()
        obj.type = self.name
        obj.name = '__json'
        obj.initial_value = 'NULL'
        obj.is_static = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

        method = Function()
        method.name = 'shared'
        method.return_type = self.name
        method.is_static = True
        method.translated = True
        method.operations.extend(SHARED_METHOD.split('\n'))
        self.functions.append(method)
        
        method = Function()
        method.name = 'deserialize_xml'
        method.args.append(['xml', ''])
        self.functions.append(method)
        method = Function()
        method.name = 'deserialize_json'
        method.args.append(['xml', ''])
        self.functions.append(method)

        method = Function()
        method.name = 'serialize_xml'
        method.args.append(['xml', ''])
        self.functions.append(method)
        method = Function()
        method.name = 'serialize_json'
        method.args.append(['xml', ''])
        self.functions.append(method)

    def create_getters(self, classes):
        for class_ in classes:
            if class_.is_storage and (class_.side == self.parser.side or class_.side == 'both'):
                map_name = get_data_list_name(get_data_name(class_.name))
                method = Function()
                method.name = 'get' + class_.name
                method.args.append(['name', ''])
                method.operations.append(PATTERN_GETTER)
                method.operations[0] = method.operations[0].replace('@{array}', map_name)
                method.operations[0] = method.operations[0].replace('@{type}', class_.name)
                self.functions.append(method)

                method = Function()
                method.name = 'loadAll' + get_data_list_name(class_.name)
                method.operations.append(PATTERN_LOAD_ALL)
                method.operations[0] = method.operations[0].replace('@{array}', map_name)
                method.operations[0] = method.operations[0].replace('@{type}', class_.name)
                self.functions.append(method)

    def add_initialize_function_json(self):
        method = Function()
        method.name = 'initialize_json'
        method.return_type = 'void'
        method.is_const = True
        method.args.append(['content', 'string'])
        method.translated = True

        method.operations.append('$json = json_decode(content);')
        method.operations.append('$this->deserialize(json);')
        method.operations.append('$this->_loaded = true;')
        self.functions.append(method)

    def add_initialize_function_xml(self):
        method = Function()
        method.name = 'initialize_xml'
        method.return_type = 'void'
        method.is_const = True
        method.args.append(['content', 'string'])
        method.translated = True

        method.operations.append('$root = simplexml_load_string(content);')
        method.operations.append('$this->deserialize(root);')
        method.operations.append('$this->_loaded = true;')
        self.functions.append(method)


SHARED_METHOD = '''
if(DataStorage::$__instance == NULL)
{
    function endsWith($haystack, $needle)
    {
        //https://stackoverflow.com/questions/834303/startswith-and-endswith-functions-in-php
        // search forward starting from end minus needle length characters
        if ($needle === '')
        {
            return true;
        }
        $diff = \strlen($haystack) - \strlen($needle);
        return $diff >= 0 && strpos($haystack, $needle, $diff) !== false;
    }

    DataStorage::$__instance = new DataStorage();
    if(endsWith(DataStorage::$PATH_TO_DATA, '.xml'))
    {
        DataStorage::$__xml = simplexml_load_file(DataStorage::$PATH_TO_DATA);
    }
    else if(endsWith(DataStorage::$PATH_TO_DATA, '.json'))
    {
        $string = file_get_contents(DataStorage::$PATH_TO_DATA);
        DataStorage::$__json = json_decode($string);
    }

}
return DataStorage::$__instance;
'''

PATTERN_GETTER = '''
    if (array_key_exists($name, $this->@{array}))
    {
        return $this->@{array}[$name];
    }
    else if(DataStorage::$__xml != null)
    {
        $data = new @{type}();
        if(DataStorage::$__xml->@{array})
        {
            foreach (DataStorage::$__xml->@{array}->pair as $node)
            {
                if ($node["key"] == $name)
                {
                    $this->@{array}[$name] = $data;
                    $data->deserialize_xml($node->value);
                }
            }
        }
        return $data;
    }
    else if(DataStorage::$__json != null)
    {
        $data = new @{type}();
        if(DataStorage::$__json->@{array})
        {
            foreach (DataStorage::$__json->@{array} as $node)
            {
                if ($node->key == $name)
                {
                    $this->@{array}[$name] = $data;
                    $data->deserialize_json($node->value);
                }
            }
        }
        return $data;
    }
    '''

PATTERN_LOAD_ALL = '''
    if(DataStorage::$__xml != null && DataStorage::$__xml->@{array})
    {
        foreach (DataStorage::$__xml->@{array}->pair as $node)
        {
            $name = (string)$node["key"];
            $this->@{array}[$name] = new @{type}();
            $this->@{array}[$name]->deserialize_xml($node->value);
        }
    }
    else if(DataStorage::$__json != null && DataStorage::$__json->@{array})
    {
        foreach (DataStorage::$__json->@{array} as $node)
        {
            $name = (string)$node->key;
            $this->@{array}[$name] = new @{type}();
            $this->@{array}[$name]->deserialize_json($node->value);
        }
    }
    '''