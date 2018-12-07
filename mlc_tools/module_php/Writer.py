from ..base import WriterBase
from ..core.Object import *
from .Serializer import Serializer


class Writer(WriterBase):

    def __init__(self, out_directory):
        WriterBase.__init__(self, out_directory)

    def write_class(self, cls):

        self.set_initial_values(cls)

        declaration_list = ''
        initialization_list = ''
        for member in cls.members:
            declare, init = self.write_object(member)
            declaration_list += declare + '\n'
            if init:
                initialization_list += init + '\n'
        
        functions = ''
        for method in cls.functions:
            f = self.write_function(method)
            functions += f
        
        imports = ''
        name = cls.name
        extend = ''
        include_patter = '\nrequire_once "{}.php";'
        if cls.superclasses:
            extend = ' extends ' + cls.superclasses[0].name
            imports += include_patter.format(cls.superclasses[0].name)
        for obj in cls.members:
            if self.model.get_class(obj.type):
                if obj.type != cls.name:
                    imports += include_patter.format(obj.type)
            elif obj.type == 'list' or obj.type == 'map':
                for arg in obj.template_args:
                    if self.model.get_class(arg.type) and arg.type != cls.name:
                        imports += include_patter.format(arg.type)
        imports += include_patter.format('Factory')
        if 'DataStorage' in functions:
            imports += include_patter.format('DataStorage')

        out = PATTERN_FILE.format(name=name,
                                  extend=extend,
                                  declarations=declaration_list,
                                  initialize_list=initialization_list,
                                  functions=functions,
                                  imports=imports,
                                  )

        return [
            ('%s.php' % cls.name, self.prepare_file(out))
            ]

    def set_initial_values(self, cls):
        if cls.type == 'enum':
            for member in cls.members:
                if member.name == '_value' and member.initial_value is not None:
                    member.initial_value = cls.members[0].initial_value

    def write_function(self, method):
        args = []
        for name, arg in method.args:
            if arg.initial_value is not None:
                args.append('$' + name + '=' + Serializer.convert_initialize_value(arg.initial_value))
            else:
                args.append('$' + name)
        args = ', '.join(args)

        text = PATTERN_METHOD.format(name=method.name,
                                     args=args,
                                     body=method.body)
        if method.is_static:
            text = 'static ' + text
        return text
    
    def write_object(self, obj):
        out_init = ''
        value = obj.initial_value
        if value is None and not obj.is_pointer:
            if obj.type == "string":
                value = '""'
            elif obj.type == "int":
                value = "0"
            elif obj.type == "float":
                value = "0"
            elif obj.type == "uint":
                value = "0"
            elif obj.type == "bool":
                value = "False"
            elif obj.type == "list":
                value = "array()"
            elif obj.type == "map":
                value = "array()"
            else:
                if self.model.get_class(obj.type):
                    value = 'null'
                    out_init = '$this->{} = new {}();'.format(obj.name, obj.type)
        else:
            cls = self.model.get_class(obj.type)
            if cls and cls.type == 'enum':
                value = None
                out_init = '$this->{} = {};'.format(obj.name, Serializer.convert_initialize_value(obj.initial_value))
    
        accesses = {
            AccessSpecifier.public: 'public',
            AccessSpecifier.protected: 'protected',
            AccessSpecifier.private: 'private',
        }
    
        if obj.is_static:
            out_declaration = accesses[obj.access] + ' static ${0} = {1};'
        else:
            out_declaration = accesses[obj.access] + ' ${0} = {1};'
        out_declaration = out_declaration.format(obj.name, Serializer.convert_initialize_value(value))
        return out_declaration, out_init
    
    def prepare_file(self, text):
        text = text.replace('::TYPE', '::$TYPE')
        text = text.replace('nullptr', 'null')

        tabs = 0
        lines = text.split('\n')
        text = list()

        def get_tabs(count):
            out = ''
            for index in range(count):
                out += '\t'
            return out

        for line in lines:
            line = line.strip()

            if line and line[0] == '}':
                tabs -= 1
            line = get_tabs(tabs) + line
            if line.strip() and line.strip()[0] == '{':
                tabs += 1
            text.append(line)
        text = '\n'.join(text)
        for i in range(10):
            tabs = '\n'
            for k in range(i):
                tabs += '\t'
            tabs += '{'
            text = text.replace(tabs, ' {')
        text = text.replace('foreach(', 'foreach (')
        text = text.replace('for(', 'for (')
        text = text.replace('if(', 'if (')
        text = text.replace('  extends', ' extends')
        text = text.strip()
        return text


PATTERN_FILE = '''<?php
{imports}

class {name} {extend}
{{
    //members:
    {declarations}
    
    public function __construct()
    {{
        {initialize_list}
    }}
    
    //functions
    {functions}
}};

?>
'''

PATTERN_METHOD = '''function {name}({args})
{{
    {body}
}}
'''