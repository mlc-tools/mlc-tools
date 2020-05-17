from ..base import WriterBase
from ..core.object import AccessSpecifier
from .serializer import Serializer


class Writer(WriterBase):

    def __init__(self, out_directory):
        WriterBase.__init__(self, out_directory)

    def write_class(self, cls):
        self.set_initial_values(cls)

        declaration_list = ''
        initialization_list = ''
        static_initialization_list = ''
        for member in cls.members:
            declare, init, static_init = self.write_object(member)
            declaration_list += declare + '\n'
            if init:
                initialization_list += init + '\n'
            if static_init:
                static_initialization_list += static_init + '\n'

        functions = ''
        for method in cls.functions:
            text = self.write_function(method)
            functions += text

        imports = ''
        name = cls.name
        extend = ''
        include_patter = '\nrequire_once "{}.php";'
        if cls.superclasses:
            extend = ' extends ' + cls.superclasses[0].name
            imports += include_patter.format(cls.superclasses[0].name)
        for obj in cls.members:
            if self.model.has_class(obj.type):
                if obj.type != cls.name:
                    imports += include_patter.format(obj.type)
            elif obj.type in ['list', 'map']:
                for arg in obj.template_args:
                    if self.model.has_class(arg.type) and arg.type != cls.name:
                        imports += include_patter.format(arg.type)
        imports += include_patter.format('Factory')
        if 'DataStorage' in functions:
            imports += include_patter.format('DataStorage')

        constructor_args, constructor_body = self.get_constructor_data(cls)
        out = PATTERN_FILE.format(name=name,
                                  extend=extend,
                                  declarations=declaration_list,
                                  initialize_list=initialization_list,
                                  static_initialization=static_initialization_list,
                                  functions=functions,
                                  imports=imports,
                                  constructor_args=constructor_args,
                                  constructor_body=constructor_body)
        return [
            ('%s.php' % cls.name, self.prepare_file(out))
        ]

    def write_object(self, obj) -> (str, str or None, str or None):
        static_initialization = None
        constructor_initialization = None
        declaration = None
        value = obj.initial_value
        cls_type = self.model.get_class(obj.type) if self.model.has_class(obj.type) else None
        if (value in [None, '"NONE"'] and not obj.is_pointer) or (cls_type and cls_type.type == 'enum'):
            if obj.type == "string":
                value = '""'
            elif obj.type == "int":
                value = "0"
            elif obj.type == "float":
                value = "0"
            elif obj.type == "uint":
                value = "0"
            elif obj.type == "bool":
                value = "false"
            elif obj.type == "list":
                value = "array()"
            elif obj.type == "map":
                value = "array()"
            else:
                if cls_type is not None and cls_type.type == 'enum':
                    value = None
                    if obj.initial_value:
                        initial_value = obj.initial_value.replace('::', '::$')
                    else:
                        initial_value = '{}::${}'.format(cls_type.name, cls_type.members[0].name)
                    constructor_initialization = '$this->{} = {};'.format(obj.name, initial_value)
                elif cls_type:
                    constructor_initialization = '$this->{} = new {}();'.format(obj.name, obj.type)

        if obj.is_static:
            if self.model.has_class(obj.type) and value and value not in ['null', 'NULL']:
                if not obj.is_pointer:
                    value = 'new ' + value
                static_initialization = '{}::${} = {};'
                declaration = ' static ${0};'
            # if not  and obj.type in ['list', 'map', 'int', 'bool', 'float', 'string']:
            else:
                declaration = AccessSpecifier.to_string(obj.access) + ' static ${0} = {1};'
        else:
            declaration = AccessSpecifier.to_string(obj.access) + ' ${0} = {1};'

        declaration = declaration.format(obj.name, Serializer().convert_initialize_value(value))
        if static_initialization:
            static_initialization = static_initialization.format(self.current_class.name,
                                                                 obj.name,
                                                                 Serializer().convert_initialize_value(value))
        return declaration, constructor_initialization, static_initialization

    def prepare_file(self, text):
        text = self.prepare_file_codestype_php(text)
        text = text.replace('::TYPE', '::$TYPE')
        text = text.replace('nullptr', 'null')
        text = text.replace('foreach(', 'foreach (')
        text = text.replace('for(', 'for (')
        text = text.replace('if(', 'if (')
        text = text.replace('  extends', ' extends')
        text = text.strip()
        return text

    def get_method_arg_pattern(self, obj):
        return '{type} ${name}={value}' if obj.initial_value is not None else '{type} ${name}'

    def get_method_pattern(self, method):
        return PATTERN_METHOD

    def get_required_args_to_function(self, method):
        return None

    def add_static_modifier_to_method(self, text):
        return 'static ' + text


PATTERN_FILE = '''<?php
{imports}

class {name} {extend}
{{
    //members:
    {declarations}
    
    public function __construct({constructor_args})
    {{
        {initialize_list}
        {constructor_body}
    }}
    
    //functions
    {functions}
}};
{static_initialization}

?>
'''

PATTERN_METHOD = '''{access} function {name}({args})
{{
    {body}
}}
'''
