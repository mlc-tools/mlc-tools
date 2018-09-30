from .Writer import Writer
from .Function import Function
from .Class import Class
from .DataStorageCreators import DataStoragePhpXml
from .DataStorageCreators import DataStoragePhpJson
from .Error import Error
from .Object import AccessSpecifier
from .regex import RegexPatternPhp
import re

SERIALIZATION = 0
DESERIALIZATION = 1


def convertInitializeValue(value):
    if value and value.startswith('this'):
        value = '$' + value
    if value is None:
        value = 'null'
    if isinstance(value, str):
        value = RegexPatternPhp.INITIALIZE[0].sub(RegexPatternPhp.INITIALIZE[1], value)
    return value


class WriterPhp(Writer):

    def __init__(self, parser, serialize_format):
        self.functions_cache = {}
        self.save_visitors = False
        Writer.__init__(self, parser, serialize_format)

    def save_generated_classes(self, out_directory):
        Writer.save_generated_classes(self, out_directory)
        self.create_factory()
        self.create_visitor_acceptors()

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
        if cls.superclasses:
            extend = ' extends ' + cls.superclasses[0].name
            imports += include_patter.format(cls.superclasses[0].name)
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
        if cls.name not in self.functions_cache:
            self.functions_cache[cls.name] = []
        if function.name == 'visit' and \
                ((cls.superclasses and cls.superclasses[0].name.startswith('IVisitor')) or cls.name.startswith('IVisitor'))\
                and function.args and len(function.args[0]) > 1:
            ctx_name = function.args[0][1]
            ctx_name = ctx_name[0].lower() + ctx_name[1:]
            ctx_name = ctx_name.replace('*', '')
            function.name = 'visit_' + ctx_name

        if function.name in self.functions_cache[cls.name]:
            Error.warning(Error.DUBLICATE_METHODS, cls.name, function.name)
            return ''
        self.functions_cache[cls.name].append(function.name)
        convert = function.name not in generated_functions and self.current_class.name != 'DataStorage'

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
        else:
            cls = self.parser.find_class(object.type)
            if cls and cls.type == 'enum':
                value = None
                out_init = '$this->{} = {};'.format(object.name, convertInitializeValue(object.initial_value))

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

    def _get_filename_of_class(self, cls):
        return cls.name + ".php"

    def get_serialiation_function_args(self):
        return self.serialize_format

    def create_serialization_function(self, cls, serialize_type):
        function = Function()
        function.name = 'serialize' if serialize_type == SERIALIZATION else 'deserialize'
        for func in cls.functions:
            if func.name == function.name:
                return

        function.args = [[self.get_serialiation_function_args(), None]]

        if len(cls.superclasses):
            function.operations.append('parent::{}(${});'.format(function.name, self.get_serialiation_function_args()))
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
        
        def get_create_type_operation(type_):
            types = {
                'list': 'array',
                'map': 'array',
            }
            return types[type_] if type_ in types else 'new ' + type_
        
        if value_type not in self.parser.simple_types:
            value_declararion = '$value = {}();'.format(get_create_type_operation(value_type))
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
        cls = self.parser.find_class(type)
        arg_0 = obj_template_args[0].type if len(obj_template_args) > 0 else 'unknown_arg'
        if cls and cls.type == 'enum':
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
                        type = "list<pointer>"
                    elif arg.type == 'enum':
                        type = 'list<string>'
                        arg_0 = 'string'
                    else:
                        type = "list<serialized>"
                        obj_type = arg_type
        fstr = self.serialize_protocol[serialization_type][type][index]
        return fstr.format(obj_name, obj_type, obj_value, '{}', owner, arg_0)

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
                require_once "$type.php";
                return new $type;
            __end__

            {0}

        __end__;

        ?>'''

        factory_methods = {}
        factory_methods['xml'] = '''static function create_command($payload)
        {
            $xml     = simplexml_load_string($payload);
            $class   = $xml->getName();
            require_once "$class.php";
            $command = new $class;
            $command->deserialize($xml);
            return $command;
        }

        static function serialize_command($command)
        {
            $xml = simplexml_load_string('<'.$command->get_type().'/>');
            $command->serialize($xml);
            return $xml->asXML();
        }'''

        factory_methods['json'] = '''static function create_command($payload)
        {
            $json    = json_decode($payload);
            $class   = key($json);
            require_once "$class.php";
            $command = new $class;
            $command->deserialize($json->$class);
            return $command;
        }

        static function serialize_command($command)
        {
            $type = $command->get_type();
            $json = json_decode('{"'.$type.'": {}}');
            $command->serialize($json->$type);
            return json_encode($json, JSON_PRETTY_PRINT);
        }'''

        factory = pattern.format(factory_methods[self.serialize_format])
        self.save_file('Factory.php', factory)

    def create_visitor_acceptors(self):
        self.save_visitors = True
        pattern = _pattern_visitor
        line = 'else if($ctx->get_type() == {0}::$TYPE)\n@(\n$this->visit_{1}($ctx);\n@)\n'
        line_import = 'require_once "{0}.php";\n'
        line_visit = '''\nfunction visit_{0}($ctx)\n@(\n@)\n'''
        base_visitors = {}
        for cls in self.parser.classes:
            if cls.is_visitor and (not cls.superclasses[0].is_visitor if len(cls.superclasses) else True):
                base_visitors[cls] = []
        for cls in self.parser.classes:
            superclass = cls.superclasses[0] if cls.superclasses else None
            while superclass:
                if superclass in base_visitors:
                    base_visitors[superclass].append(cls)
                    break
                superclass = superclass.superclasses[0] if superclass.superclasses else None
        for superclass in base_visitors:
            lines = ''
            visits = ''
            imports = ''
            for cls in base_visitors[superclass]:
                if self.parser.is_visitor(cls):
                    func_name = cls.name
                    func_name = func_name[0].lower() + func_name[1:]

                    lines += line.format(cls.name, func_name)
                    imports += line_import.format(cls.name)
                    visits += line_visit.format(func_name)
            name = 'IVisitor{}'.format(superclass.name)
            body = pattern.format(imports, lines, visits, name)
            body = body.replace('@(', '{')
            body = body.replace('@)', '}')
            self.save_file(name + '.php', body)

    def create_data_storage_class(self, name, classes):
        if self.serialize_format == 'xml':
            return DataStoragePhpXml(name, classes, self.parser)
        else:
            return DataStoragePhpJson(name, classes, self.parser)

    def prepare_file(self, body):
        body = body.replace('__begin__', '{')
        body = body.replace('__end__', '}')
        body = body.replace('::TYPE', '::$TYPE')
        body = body.replace('nullptr', 'null')

        tabs = 0
        lines = body.split('\n')
        body = list()

        def get_tabs(count):
            out = ''
            for i in range(count):
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
        for i in range(10):
            tabs = '\n'
            for k in range(i):
                tabs += '\t'
            tabs += '{'
            body = body.replace(tabs, ' {')
        body = body.replace('foreach(', 'foreach (')
        body = body.replace('for(', 'for (')
        body = body.replace('if(', 'if (')
        body = body.replace('  extends', ' extends')
        body = body.strip()
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
                member.type = use_type

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

    def save_file(self, filename, string):
        if not self.save_visitors and filename.startswith('IVisitor'):
            return
        Writer.save_file(self, filename, string)


def convert_function_to_php(func, parser, function_args):
    if not func and not function_args:
        return func
    repl = (
        ('$if(', 'if('),
        ('function $', 'function '),
        ('($int)', '(int)'),
        ('time(nullptr)', 'time()'),
        ('$$', '$'),
        ('std::max', 'max'),
        ('std::$max<int>', 'max'),
        ('std::$max<float>', 'max'),
        ('std::min', 'min'),
        ('std::$min<int>', 'min'),
        ('std::$min<float>', 'min'),
        ('std::round', 'round'),
        ('std::floor', 'floor'),
        ('std::fabs', 'abs'),
        ('std::ceil', 'ceil'),
        ('std::sqrt', 'sqrt'),
        ('in_list(', 'in_array('),
        ('in_map', 'array_key_exists'),
        ('list_push', 'array_push'),
        ('list_size', 'count'),
        ('map_size', 'count'),
    )

    strings = []
    string_pattern = '@{__string_%d__}'
    while '"' in func:
        l = func.index('"')
        r = l + 1
        p = ''
        while r < len(func):
            if func[r] == '"' and p != '\\':
                string = func[l:r + 1]
                func = func[:l] + string_pattern % len(strings) + func[r + 1:]
                strings.append(string)
                break
            p = func[r]
            r += 1

    for reg in RegexPatternPhp.FUNCTION:
        func = reg[0].sub(reg[1], func)

    for key in RegexPatternPhp.VARIABLES:
        patterns_dict = RegexPatternPhp.VARIABLES[key]
        arr = key.findall(function_args + '\n' + func)
        dividers = ' +-*\\=()[]<>\t\n!,.;'
        for var in arr:
            for ch in dividers:
                i = 0
                while i < len(func):
                    replace = False
                    full = ch + var
                    start = func.find(full, i)
                    if start == -1:
                        break
                    next = start + len(full)
                    i = next
                    if next < len(func):
                        replace = func[next] in dividers
                    if not replace:
                        continue
                    # func = func.replace(ch + var, ch + '$' + var)
                    func = func[:start] + (ch + '$' + var) + func[next:]

            pattern = '^' + var
            if pattern not in patterns_dict:
                patterns_dict[pattern] = re.compile(pattern)
            pattern = patterns_dict[pattern]

            func = pattern.sub('$' + var, func)
            for ch in ['->']:
                func = func.replace(ch + '$' + var, ch + var)

    for reg in RegexPatternPhp.FUNCTION_2:
        func = reg[0].sub(reg[1], func)

    for reg in repl:
        func = func.replace(reg[0], reg[1])

    for i, string in enumerate(strings):
        func = func.replace(string_pattern % i, string)

    for cls in parser.classes:
        if cls.name in func:
            func = 'require_once "{}.php";\n'.format(cls.name) + func

    return func


generated_functions = (
    'serialize',
    'deserialize',
    'get_type',
    'shared',
    '__toString',
    'str',
    'int',
    'set',
    's_to_int',
)
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
