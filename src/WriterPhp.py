from Writer import Writer
from Function import Function
from Class import Class
from DataStorageCreators import DataStoragePhpXml
from DataStorageCreators import DataStoragePhpJson
from Error import Error
import re
from Object import AccessSpecifier

SERIALIZATION = 0
DESERIALIZATION = 1

allowed_functions = [
    'serialize',
    'deserialize',
    'get_type',
    'shared',
    '__toString',
    'str',
    'int',
    'set',
    's_to_int',
]


def convertInitializeValue(value):
    if value and value.startswith('this'):
        value = '$' + value
    if value is None:
        value = 'null'
    return value


functions_cache = {}


class WriterPhp(Writer):

    def __init__(self, parser, serialize_format):
        Writer.__init__(self, parser, serialize_format)
        self.current_class = None

    def save_generated_classes(self, out_directory):
        Writer.save_generated_classes(self, out_directory)
        self.create_factory()
        self.create_visitor_acceptors()
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

        declaration_list = ''
        initialization_list = ''
        for object in cls.members:
            declare, init = self.write_object(object)
            declaration_list += declare + '\n'
            if init:
                initialization_list += init + '\n'

        self.create_serialization_function(cls, SERIALIZATION)
        self.create_serialization_function(cls, DESERIALIZATION)
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
        if 'DataStorage' in functions:
            imports += include_patter.format('DataStorage')

        out = pattern.format(name, extend, declaration_list, functions, imports, initialization_list)
        self.current_class = None
        return {flags: out}

    def write_function(self, cls, function):
        global functions_cache
        if cls.name not in functions_cache:
            functions_cache[cls.name] = []
        if function.name in functions_cache[cls.name]:
            Error.warning(Error.DUBLICATE_METHODS, cls.name, function.name)
            return ''
        functions_cache[cls.name].append(function.name)
        convert = function.name not in allowed_functions and self.current_class.name != 'DataStorage'

        out = '''function {0}({1})
        __begin__
        {2}
        __end__\n'''

        if function.is_static:
            out = 'public static ' + out
        else:
            out = 'public ' + out

        name = function.name
        args = ', '.join(['$' + x[0] for x in function.args])
        ops = '\n'.join(function.operations)
        if convert:
            ops = convert_function_to_php(ops, self.parser, args)
        out = out.format(name, args, ops)
        return out

    def write_object(self, object):
        out_declaration = ''
        out_init = ''
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
            else:
                if self.parser.find_class(object.type):
                    value = 'null'
                    out_init = '$this->{} = new {}();'.format(object.name, object.type)

        accesses = {
            AccessSpecifier.public: 'public',
            AccessSpecifier.protected: 'protected',
            AccessSpecifier.private: 'private',
        }

        if object.is_static:
            out_declaration = accesses[object.access] + ' static ${0} = {1};'
        else:
            out_declaration = accesses[object.access] + ' ${0} = {1};'
        out_declaration = out_declaration.format(object.name, convertInitializeValue(value))
        return out_declaration, out_init

    def _getImports(self, cls):
        return ""

    def _get_filename_of_class(self, cls):
        return cls.name + ".php"

    def get_serialiation_function_args(self):
        if self.serialize_format == 'xml':
            return 'xml'
        return 'json'

    def create_serialization_function(self, cls, serialize_type):
        function = Function()
        function.name = 'serialize' if serialize_type == SERIALIZATION else 'deserialize'
        for func in cls.functions:
            if func.name == function.name:
                return

        function.args = [[self.get_serialiation_function_args(), None]]

        if cls.behaviors:
            if self.serialize_format == 'xml':
                function.operations.append('parent::{}($xml);'.format(function.name))
            else:
                function.operations.append('parent::{}($json);'.format(function.name))
        for obj in cls.members:
            if obj.is_runtime:
                continue
            if obj.is_static:
                continue
            if obj.is_const and not obj.is_link:
                continue

            line = self.build_serialize_operation(obj.name, obj.type, obj.initial_value, serialize_type,
                                                  obj.template_args, obj.is_pointer, is_link=obj.is_link)
            function.operations.append(line)

        cls.functions.append(function)

    def build_map_serialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args, serialization_type):
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
        a1 = self.build_serialize_operation('key', key_type, None, serialization_type, key.template_args, False, '$', key.is_link)
        a2 = self.build_serialize_operation('value', value_type, None, serialization_type, value.template_args, _value_is_pointer, '$', False)
        a1 = a1.split('\n')
        for index, a in enumerate(a1):
            a1[index] = a
        a1 = '\n'.join(a1)
        a2 = a2.split('\n')
        for index, a in enumerate(a2):
            a2[index] = a
        a2 = '\n'.join(a2)
        return str.format(a0, a1, a2, '{}', '$this->', value_declararion) + '\n'

    def build_serialize_operation(self, obj_name, obj_type, obj_value, serialization_type, obj_template_args,
                                  obj_is_pointer, owner='$this->', is_link=False):
        index = 0
        if obj_value is None:
            index = 1
        type = obj_type
        if self.parser.find_class(type) and self.parser.find_class(type).type == 'enum':
            type = 'enum'
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
                        Error.exit(Error.MAP_TWO_ARGS, self._current_class.name, obj_name)
                    return self.build_map_serialization(obj_name, obj_type, obj_value, obj_is_pointer,
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
                    elif arg.type == 'enum':
                        type = 'list<string>'
                    else:
                        type = "list<serialized>"
                        obj_type = arg_type
        fstr = self.serialize_protocol[serialization_type][type][index]
        return fstr.format(obj_name, obj_type, obj_value, '{}', owner,
                           obj_template_args[0].type if len(obj_template_args) > 0 else 'unknown_arg')

    def save_config_file(self):
        content = '''<?php\n
$MG_XML = 1;
$MG_JSON = 2;
$MG_SERIALIZE_FORMAT = $MG_{};
\n?>
        '''.format(self.serialize_format.upper())
        self.save_file('config.php', content)

    def create_factory(self):
        pattern = '''<?php

class Factory
__begin__
    static function build($type)
    __begin__
        {0}
    __end__
__end__;

?>'''
        factory = pattern.format('require_once "$type.php"; \n return new $type;')
        self.save_file('Factory.php', factory)

    def create_visitor_acceptors(self):
        pattern = _pattern_visitor
        line = '        else if($ctx->get_type() == {0}::$TYPE)\n@(\n$this->visit_{1}($ctx);\n@)\n'
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
            self.save_file(name + '.php', body)

    def create_data_storage_class(self, name, classes):
        if self.serialize_format == 'xml':
            return DataStoragePhpXml(name, classes, self.parser)
        else:
            return DataStoragePhpJson(name, classes, self.parser)
        pass

    def prepare_file(self, body):
        body = body.replace('__begin__', '{')
        body = body.replace('__end__', '}')
        body = body.replace('::TYPE', '::$TYPE')

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
            line = get_tabs(tabs) + line
            if line.strip() and line.strip()[0] == '{':
                tabs += 1
            body.append(line)
        body = '\n'.join(body)
        for i in xrange(10):
            tabs = '\n'
            for k in xrange(i):
                tabs += '\t'
            tabs += '{'
            body = body.replace(tabs, ' {')
        body = body.replace('foreach(', 'foreach (')
        body = body.replace('for(', 'for (')
        body = body.replace('if(', 'if (')
        body = body.replace('  extends', ' extends')
        return body

    def create_data_storage(self):
        storage = self.create_data_storage_class('DataStorage', self.parser.classes)
        content = self.write_class(storage, 0)[0]
        self.save_file(storage.name + '.php', content)

    def convert_to_enum(self, cls, use_type='string'):
        Writer.convert_to_enum(self, cls, use_type)
        function = Function()
        function.name = '__toString'
        function.operations.append('return $this->_value;')
        cls.functions.append(function)

        function = Function()
        function.name = 'str'
        function.operations.append('return (string)$this;')
        cls.functions.append(function)

        for i, member in enumerate(cls.members):
            if member.name == '_value':
                member.type = 'string'

        function = Function()
        function.name = 'set'
        function.args.append(['value', ''])
        function.operations.append('$this->_value = $value;')
        cls.functions.append(function)

        function = Function()
        function.name = 'serialize'
        cls.functions.append(function)

        function = Function()
        function.name = 'deserialize'
        cls.functions.append(function)


regs = [
    [re.compile('DataStorage::shared\(\).get<(\w+)>'), 'DataStorage::shared()->get\\1'],
    [re.compile('\\.str\\(\\)'), ''],
    [re.compile('for\s*\\(auto (.+?)\s*:\s*(.+?)\s*\\)'), 'foreach($\\2 as $\\1)'],
    [re.compile('for\s*\\(auto& (.+?)\s*:\s*(.+?)\s*\\)'), 'foreach($\\2 as $\\1)'],
    [re.compile('for\s*\\(auto&&\s*\\[(\w+),\s*(\w+)\\]\s*:\s*(.+)\\)'), 'foreach ($\\3 as $\\1 => $\\2)'],
    [re.compile('auto (\w+)'), '$\\1'],
    [re.compile('auto& (\w+)'), '$\\1'],
    [re.compile('void (\w+)'), '$\\1'],
    [re.compile('int (\w+)'), '$\\1'],
    [re.compile('bool (\w+)'), '$\\1'],
    [re.compile('\\((\w+) (\w+)\\)'), '($\\2)'],
    [re.compile('\\(const (\w+)\\& (\w+)\\)'), '($\\2)'],
    [re.compile('\\(const (\w+)\\* (\w+)\\)'), '($\\2)'],
    [re.compile('\\((\w+)\\* (\w+)\\)'), '($\\2)'],
    [re.compile('(\w+)\\ (\w+),'), '$\\2,'],
    [re.compile('(\w+)\\& (\w+),'), '$\\2,'],
    [re.compile('(\w+)\\* (\w+),'), '$\\2,'],
    [re.compile('const (\w+)\\* (\w+)'), '$\\2'],
    [re.compile('const (\w+)\\& (\w+)'), '$\\2'],
    [re.compile('float (\w+)'), '$\\1'],
    [re.compile('std::string (\w+)'), '$\\1'],
    [re.compile('this->'), '$this->'],
    [re.compile(':const'), ''],
    [re.compile('(\w+)::(\w+)'), '\\1::$\\2'],
    [re.compile('(\w+)::(\w+)\\)'), '\\1::$\\2)'],
    [re.compile('(\w+)::(\w+)\\.'), '\\1::$\\2.'],
    [re.compile('(\w+)::(\w+)->'), '\\1::$\\2->'],
    [re.compile('(\w+)::(\w+)\\]'), '\\1::$\\2]'],
    [re.compile('(\w+)::\\$(\w+)\\((\w*)\\)'), '\\1::\\2(\\3)'],
    [re.compile('function \\$(\w+)'), 'function \\1'],
    [re.compile('\\.at\\((.*?)\\)'), '[\\1]'],

    [re.compile('(\w+)\\.'), '\\1->'],
    [re.compile('(\w+)\\(\\)\\.'), '\\1()->'],
    [re.compile('(\w+)\\]\.'), '\\1]->'],
    [re.compile('&(\w+)'), '\\1'],
    [re.compile('\\$if\\('), 'if('],
    [re.compile('delete (\w+);'), ''],
    [re.compile('([-0-9])->([-0-9])f\\b'), '\\1.\\2'],
    [re.compile('assert\\(.+\\);'), ''],
    [re.compile('make_intrusive<(\w+)>\\(\s*\\)'), 'new \\1()'],
    [re.compile('new\s*(\w+)\s*\\(\s*\\)'), 'new \\1()'],
    [re.compile('(.+?)\\->push_back\\((.+)\\);'), 'array_push(\\1, \\2);'],
]


def convert_function_to_php(func, parser, function_args):
    global regs
    variables = {
        '\$(\w+)'
    }

    regs2 = [
        ['->\\$(\w+)\\(', '->\\1('],
        ['([-0-9]*)->([-0-9]*)f\\b', '\\1.\\2'],
        ['([-0-9]*)->f\\b', '\\1.0'],
        [re.compile('\\$return\s'), 'return'],
    ]

    repl = [
        ['$if(', 'if('],
        ['function $', 'function '],
        ['($int)', '(int)'],
        ['time(nullptr)', 'time()'],
        ['$$', '$'],
        ['std::$max', 'max'],
        ['std::$min', 'min'],
        ['std::$round', 'round'],
        ['in_list(', 'in_array('],
        ['in_map', 'array_key_exists'],
        ['list_push', 'array_push'],
        ['list_size', 'count'],
        ['map_size', 'count'],
        ['nullptr', 'null'],
    ]

    for reg in regs:
        func = re.sub(reg[0], reg[1], func)

    for key in variables:
        arr = re.findall(key, function_args + '\n' + func)
        for var in arr:
            for ch in ' +-*\\=([<>\t\n!':
                func = func.replace(ch + var, ch + '$' + var)
            func = re.sub('^' + var, '$' + var, func)
            for ch in ['->']:
                func = func.replace(ch + '$' + var, ch + var)

    for reg in regs2:
        func = re.sub(reg[0], reg[1], func)

    for reg in repl:
        func = func.replace(reg[0], reg[1])

    for cls in parser.classes:
        if cls.name in func:
            func = 'require_once "{}.php";\n'.format(cls.name) + func

    return func


# format(name, initialize_list, functions, imports)
_pattern_file = {}
_pattern_file['xml'] = '''<?php
{4}

class {0} {1}
__begin__
//members:
{2}
public function __construct()
__begin__
{5}
__end__
//functions
{3}
__end__;

?>'''
_pattern_file['json'] = _pattern_file['xml']

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
