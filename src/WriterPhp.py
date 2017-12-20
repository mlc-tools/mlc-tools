from Writer import Writer
from Function import Function
from Class import Class
from DataStorageCreators import DataStoragePhpXml

SERIALIZATION = 0
DESERIALIZATION = 1

allowed_functions = [
    'serialize',
    'deserialize',
    'get_type',
    'shared',
    '__toString',
    'str',
    'set',
]

def convertInitializeValue(value):
    if value and value.startswith('this'):
        value = '$' + value
    return value


class WriterPhp(Writer):

    def __init__(self, parser, serialize_format):
        Writer.__init__(self, parser, serialize_format)
        self.current_class = None

    def save_generated_classes(self, out_directory):
        Writer.save_generated_classes(self, out_directory)
        self.createFactory()
        self.createVisitorAcceptors()
        # self.create_data_storage()

    def write_class(self, cls, flags):
        global _pattern_file
        out = ""
        pattern = _pattern_file[self.serialize_format]
        self.current_class = cls

        if cls.type == 'enum':
            for member in cls.members:
                if member.initial_value is not None and member.name == '_value':
                    member.initial_value = cls.members[0].initial_value

        initialize_list = ''
        for object in cls.members:
            initialize_list += self.write_object(object) + '\n'

        self.createSerializationFunction(cls, SERIALIZATION)
        self.createSerializationFunction(cls, DESERIALIZATION)
        functions = ''
        for function in cls.functions:
            f = self.write_function(cls, function)
            functions += f

        imports = ''
        name = cls.name
        extend = ''
        include_patter = '\nrequire_once "{}.php";'
        if cls.behaviors:
            extend = ' extends ' + cls.behaviors[0].name
            imports += include_patter.format(cls.behaviors[0].name)
        for obj in cls.members:
            if self.parser.find_class(obj.type):
                if obj.type != cls.name:
                    imports += include_patter.format(obj.type)
            elif obj.type == 'list' or obj.type == 'map':
                for arg in obj.template_args:
                    if isinstance(arg, Class) and arg.name != cls.name:
                        imports += include_patter.format(arg.name)
                    elif self.parser.find_class(arg.type) and arg.type != cls.name:
                        imports += include_patter.format(arg.type)
        imports += include_patter.format('Factory')

        out = pattern.format(name, extend, initialize_list, functions, imports)
        self.current_class = None
        return {flags: out}

    def write_function(self, cls, function):
        if function.name not in allowed_functions and self.current_class.name != 'DataStorage':
            return ''

        out = '''public function {0}({1})
        __begin__
        {2}
        __end__\n'''
        name = function.name
        args = ', '.join(['$' + x[0] for x in function.args])
        ops = '\n'.join(function.operations)
        out = out.format(name, args, ops)

        return out

    def write_object(self, object):
        out = ''
        value = object.initial_value
        if value is None and not object.is_pointer:
            type = object.type
            if type == "string":
                value = '""'
            elif type == "int":
                value = "0"
            elif type == "float":
                value = "0"
            elif type == "uint":
                value = "0"
            elif type == "bool":
                value = "False"
            elif type == "list":
                value = "array()"
            elif type == "map":
                value = "array()"

        if object.is_static:
            out = 'public static ${0} = {1};'
        else:
            out = 'public ${0} = {1};'
        out = out.format(object.name, convertInitializeValue(value))
        return out

    def _getImports(self, cls):
        return ""

    def _get_filename_of_class(self, cls):
        return cls.name + ".php"

    def getSerialiationFunctionArgs(self):
        if self.serialize_format == 'xml':
            return 'xml'
        return 'json'

    def createSerializationFunction(self, cls, serialize_type):
        function = Function()
        function.name = 'serialize' if serialize_type == SERIALIZATION else 'deserialize'
        for func in cls.functions:
            if func.name == function.name:
                return

        function.args = [[self.getSerialiationFunctionArgs(), None]]

        if cls.behaviors:
            function.operations.append('parent::{}($xml);'.format(function.name))
        for obj in cls.members:
            if obj.is_runtime:
                continue
            if obj.is_static:
                continue
            if obj.is_const and not obj.is_link:
                continue

            line = self._buildSerializeOperation(obj.name, obj.type, obj.initial_value, serialize_type, obj.template_args, obj.is_pointer, is_link=obj.is_link)
            function.operations.append(line)

        cls.functions.append(function)

    def buildMapSerialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args, serialization_type):
        key = obj_template_args[0]
        value = obj_template_args[1]
        key_type = key.name if isinstance(key, Class) else key.type
        value_type = value.name if isinstance(value, Class) else value.type
        str = self.serialize_protocol[serialization_type]['map'][0]
        _value_is_pointer = value.is_pointer
        if value_type not in self.parser.simple_types:
            value_declararion = '$value = new {}();'.format(value_type)
        else:
            value_declararion = ''
        a0 = obj_name
        a1 = self._buildSerializeOperation('key', key_type, None, serialization_type, key.template_args, False, '$', key.is_link)
        a2 = self._buildSerializeOperation('value', value_type, None, serialization_type, value.template_args, _value_is_pointer, '$', False)
        a1 = a1.split('\n')
        for index, a in enumerate(a1):
            a1[index] = a
        a1 = '\n'.join(a1)
        a2 = a2.split('\n')
        for index, a in enumerate(a2):
            a2[index] = a
        a2 = '\n'.join(a2)
        return str.format(a0, a1, a2, '{}', '$this->', value_declararion) + '\n'

    def _buildSerializeOperation(self, obj_name, obj_type, obj_value, serialization_type, obj_template_args,
                                 obj_is_pointer, owner='$this->', is_link=False):
        index = 0
        if obj_value is None:
            index = 1
        type = obj_type
        if self.parser.find_class(type) and self.parser.find_class(type).type == 'enum':
            type = 'enum'
        elif obj_type not in self.simple_types and type != "list" and type != "map":
            if is_link:
                type = 'string'
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
                    return self.buildMapSerialization(obj_name, obj_type, obj_value, obj_is_pointer,
                                                      obj_template_args, serialization_type)
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
        return fstr.format(obj_name, obj_type, obj_value, '{}', owner,
                           obj_template_args[0].type if len(obj_template_args) > 0 else 'unknown_arg')

    def save_config_file(self):
        pass
        # buffer = 'MG_XML = 2\nMG_JSON = 1\n'
        # buffer += 'MG_SERIALIZE_FORMAT = MG_' + self.serialize_format.upper()
        # buffer += '\n'
        # self.save_file('config.py', buffer)

    def createFactory(self):
        pattern = '''
<?php

class Factory
{1}
    static function build($type)
    {1}
        {0}
    {2}
{2};

?>
'''
        line = '\nif($type == "{0}")\n{1}\nrequire_once "{0}.php";\nreturn new {0}();\n{2}'
        creates = ''
        for cls in self.parser.classes:
            creates += line.format(cls.name, '{', '}')
        factory = pattern.format(creates, '{', '}')
        self.save_file('Factory.php', factory)

    def createVisitorAcceptors(self):
        pattern = _pattern_visitor
        line = '        else if($ctx->get_type() == {0}::$__type__)\n@(\n$this->visit_{1}($ctx);\n@)\n'
        line_import = 'require_once "{0}.php";\n'
        line_visit = '''\n    function visit_{0}($ctx)\n@(\n@)\n'''
        base_visitors = {}
        for cls in self.parser.classes:
            if cls.is_visitor and (cls.behaviors and not cls.behaviors[0].is_visitor):
                base_visitors[cls] = []
        for cls in self.parser.classes:
            parent = cls.behaviors[0] if cls.behaviors else None
            while parent:
                if parent in base_visitors:
                    base_visitors[parent].append(cls)
                    break
                parent = parent.behaviors[0] if parent.behaviors else None
        for parent in base_visitors:
            lines = ''
            visits = ''
            imports = ''
            for cls in base_visitors[parent]:
                if self.parser.is_visitor(cls):
                    func_name = cls.name
                    func_name = func_name[0].lower() + func_name[1:]

                    lines += line.format(cls.name, func_name)
                    imports += line_import.format(cls.name)
                    visits += line_visit.format(func_name)
            name = 'IVisitor{}'.format(parent.name)
            body = pattern.format(imports, lines, visits, name)
            body = body.replace('@(', '{')
            body = body.replace('@)', '}')
            body = self.prepare_file(body)
            self.save_file(name + '.php', body)

    def create_data_storage_class(self, name, classes):
        if self.serialize_format == 'xml':
            return DataStoragePhpXml(name, classes, self.parser)
        # else:
        #     return DataStoragePhpJson(name, classes, self.parser)
        pass

    def prepare_file(self, body):
        body = body.replace('__begin__', '{')
        body = body.replace('__end__', '}')
        body = body.replace('::__type__', '::$__type__')

        tabs = 0
        lines = body.split('\n')
        body = list()

        def get_tabs(count):
            out = ''
            for i in xrange(count):
                out += '\t'
            return out

        for line in lines:
            line = line.strip()

            if line and line[0] == '}':
                tabs -= 1
            if 'public:' in line:
                tabs -= 1
            line = get_tabs(tabs) + line
            if 'public:' in line:
                tabs += 1
            if line.strip() and line.strip()[0] == '{':
                tabs += 1
            body.append(line)
        body = '\n'.join(body)
        return body

    def create_data_storage(self):
        storage = self.create_data_storage_class('DataStorage', self.parser.classes)
        content = self.write_class(storage, 0)[0]
        content = self.prepare_file(content)
        self.save_file(storage.name + '.php', content)

    def convert_to_enum(self, cls):
        values = Writer.convert_to_enum(self, cls)
        function = Function()
        function.name = '__toString'
        for i, member in enumerate(cls.members):
            if member.name == '_value':
                continue
            function.operations.append('if($this->_value == {1}::${0})return "{0}";'.format(member.name, cls.name))
            function.operations.append('if($this->_value == {1})\n{3}\n$this->_value = {2}::${0}; return "{0}";\n{4}\n'.format(member.name, values[i], cls.name, '{', '}'))
            function.operations.append('if($this->_value == "{1}")\n{3}\n$this->_value = {2}::${0}; return "{0}";\n{4}\n;'.format(member.name, values[i], cls.name, '{', '}'))
        cls.functions.append(function)

        function = Function()
        function.name = 'str'
        function.operations.append('return (string)$this;')
        cls.functions.append(function)

        function = Function()
        function.name = 'set'
        function.args.append(['value', ''])
        for i, member in enumerate(cls.members):
            if member.name == '_value':
                continue
            function.operations.append('if($value == {1}::${0}) $this->_value = {1}::${0};'.format(member.name, cls.name))
            function.operations.append('if($value == "{2}") $this->_value = {1}::${0};'.format(member.name, cls.name, values[i]))
            function.operations.append('if($value == "{0}") $this->_value = {1}::${0};'.format(member.name, cls.name))
        cls.functions.append(function)


# format(name, initialize_list, functions, imports)
_pattern_file = {}
_pattern_file['xml'] = '''<?php
{4}

class {0} {1}
__begin__
//members:
{2}
//functions
{3}
__end__;

?>'''

_pattern_visitor = '''<?php

{0}\nclass {3}
@(
function visit($ctx)
@(
    if(0)
    @(
    @)
    {1}
@)
{2}
@);
?>'''
