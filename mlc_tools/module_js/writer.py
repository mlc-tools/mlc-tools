from ..base import WriterBase


class Writer(WriterBase):

    def __init__(self, out_directory):
        WriterBase.__init__(self, out_directory)

    def write_class(self, cls):
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
        constructor_args, constructor_body = self.get_constructor_data(cls)
        out = PATTERN_FILE.format(name=name,
                                  extend=extend,
                                  members_list=members_list.strip(),
                                  static_list=static_list.strip(),
                                  functions=functions.strip(),
                                  superclass_construct='super()' if cls.superclasses else '',
                                  constructor_args=constructor_args,
                                  constructor_body=constructor_body)
        return [('%s.js' % cls.name, self.prepare_file(out))]

    def write_object(self, obj):
        member = ''
        static = ''
        value = obj.initial_value.replace('::', '.') if obj.initial_value else None
        if (value is None or value == '"NONE"') and not obj.is_pointer:
            if obj.type == "string":
                value = '""'
            elif obj.type in ["uint", 'unsigned', 'int', 'float', 'int64_t', 'uint64_t']:
                value = "0"
            elif obj.type == "bool":
                value = "false"
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
        text = self.prepare_file_codestype_php(text)
        text = text.replace('nullptr', 'null')
        text = text.replace('NULL', 'null')
        return text

    def get_method_arg_pattern(self, obj):
        return '{name}={value}' if obj.initial_value is not None else '{name}'

    def get_method_pattern(self, method):
        return PATTERN_METHOD if not method.is_static else PATTERN_STATIC_METHOD

    def get_required_args_to_function(self, method):
        return None

    def add_static_modifier_to_method(self, text):
        return text


PATTERN_FILE = '''
class {name} {extend}
{{
    constructor({constructor_args})
    {{
        {superclass_construct}
        //members:
        {members_list}
        {constructor_body}
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
