from ..base import WriterBase


class Writer(WriterBase):

    def __init__(self, out_directory):
        WriterBase.__init__(self, out_directory)

    def write_class(self, cls):
        self.current_class = cls
        self.set_initial_values(cls)

        members_list = ''
        static_list = ''
        for member in cls.members:
            declare, static = self.write_object(member)
            members_list += declare + '\n'
            if static:
                static_list += static + '\n'

        functions = ''
        for method in cls.functions:
            text = self.write_function(method)
            if method.is_static:
                static_list += text
            else:
                functions += text

        name = cls.name
        extend = ''
        if cls.superclasses:
            extend = ' extends ' + cls.superclasses[0].name
        out = PATTERN_FILE.format(name=name,
                                  extend=extend,
                                  members_list=members_list,
                                  static_list=static_list,
                                  functions=functions,
                                  superclass_construct='super()' if cls.superclasses else '')
        return [
            ('%s.js' % cls.name, self.prepare_file(out))
        ]

    def write_object(self, obj):
        member = ''
        static = ''
        value = obj.initial_value.replace('::', '.') if obj.initial_value else None
        if (value is None or value == '"NONE"') and not obj.is_pointer:
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
                value = "[]"
            elif obj.type == "map":
                value = "{}"
            else:
                cls = self.model.get_class(obj.type) if self.model.has_class(obj.type) else None
                if cls is not None and cls.type == 'enum':
                    value = '{}.{}'.format(cls.name, cls.members[0].name)
                elif cls:
                    value = 'new {}()'.format(obj.type)
        elif value is None and obj.is_pointer:
            value = 'null'

        if obj.is_static:
            static = '{}.{} = {};'.format(self.current_class.name, obj.name, value)
        else:
            member = 'this.{} = {};'.format(obj.name, value)
        return member, static

    def prepare_file(self, text):
        text = WriterBase.prepare_file(self, text)
        text = text.replace('nullptr', 'null')
        text = text.replace('NULL', 'null')

        tabs = 0
        lines = text.split('\n')
        text = list()

        def get_tabs(count):
            return '\t' * count

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
            tabs = '\n' + '\t' * i + '{'
            text = text.replace(tabs, ' {')
        # text = text.replace('foreach(', 'foreach (')
        # text = text.replace('for(', 'for (')
        # text = text.replace('if(', 'if (')
        # text = text.replace('  extends', ' extends')
        return text

    def get_method_arg_pattern(self, obj):
        return '{}={}' if obj.initial_value is not None else '{}'

    def get_method_pattern(self, method):
        return PATTERN_METHOD if not method.is_static else PATTERN_STATIC_METHOD

    def get_required_args_to_function(self, method):
        return None

    def add_static_modifier_to_method(self, text):
        return text


PATTERN_FILE = '''

class {name} {extend}
{{
    constructor()
    {{
        {superclass_construct}
        //members:
        {members_list}
    }}
    
    //functions
    {functions}
}}

//static
{static_list}
exports.{name} = {name};

'''

PATTERN_METHOD = '''{name}({args})
{{
    {body}
}};
'''

PATTERN_STATIC_METHOD = '''
{class_name}.{name} = function ({args})
{{
    {body}
}};

'''