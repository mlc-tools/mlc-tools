import re
from .model import SerializeFormat
from ..core.object import AccessSpecifier, Object


# pylint: disable=no-self-use
# pylint: disable=unused-argument
class WriterBase(object):

    def __init__(self, out_directory):
        self.model = None
        self.serializer = None
        self.out_directory = out_directory
        self.files = []
        self.created_files = []
        self.current_class = None

    def save(self, model):
        self.model = model
        for cls in model.classes:
            if not cls.auto_generated:
                continue
            self.current_class = cls
            sources = self.write_class(cls)
            for filename, content in sources:
                self.model.add_file(cls, filename, content)

    def write_class(self, cls):
        return [('', '')]

    def set_initial_values(self, cls):
        if cls.type == 'enum':
            for member in cls.members:
                if member.name == '_value' and member.initial_value is not None:
                    member.initial_value = cls.members[0].initial_value

    def get_constructor_data(self, cls):
        constructor_args = self.get_required_args_to_function(cls.constructor)
        constructor_body = ''
        if cls.constructor is not None:
            constructor_args = self.create_function_args_string(cls.constructor)
            constructor_body = cls.constructor.body
        if constructor_args is None:
            constructor_args = ''
        return constructor_args, constructor_body

    # Function methods
    def write_function(self, method):
        if method.name == 'constructor':
            return ''
        args = self.create_function_args_string(method)
        text = self.get_method_pattern(method).format(name=method.name,
                                                      args=args,
                                                      body=method.body,
                                                      access=AccessSpecifier.to_string(method.access),
                                                      class_name=self.current_class.name)
        if method.is_static:
            text = self.add_static_modifier_to_method(text)
        return text

    def create_function_args_string(self, method):
        args = []
        if self.get_required_args_to_function(method) is not None:
            args.append(self.get_required_args_to_function(method))
        for name, arg in method.args:
            pattern = self.get_method_arg_pattern(arg)
            typename = self.get_argument_typename(arg)
            args.append(pattern.format(name=name,
                                       type=typename,
                                       value=self.serializer.convert_initialize_value(arg.initial_value)))

        for template_type in method.template_types:
            obj = Object()
            obj.name = template_type
            obj.initial_value = self.get_nullptr_string()
            pattern = self.get_method_arg_pattern(obj)
            args.append(pattern.format(name=template_type, type='', value=self.get_nullptr_string()))

        args = ', '.join(args)
        return args

    # arg: Object
    def get_argument_typename(self, arg):
        typename = arg.type
        std_types = {
            'string': 'string',
            'int': 'int',
            'float': 'float',
            'bool': 'bool',
            'void': '',
        }
        if typename in std_types:
            return std_types[typename]
        if self.model.has_class(typename):
            return typename
        return ''

    def get_method_arg_pattern(self, obj):
        return '${name}={value}' if obj.initial_value is not None else '${name}'

    def get_method_pattern(self, method):
        return '{name}({args})\n{body}'

    def get_required_args_to_function(self, method):
        return None

    def get_nullptr_string(self):
        return 'null'

    def add_static_modifier_to_method(self, text):
        return 'static ' + text

    # End Function methods

    def write_object(self, obj):
        return ''

    def prepare_file(self, text):

        def remove_content(txt, obj_type):
            pattern = re.compile(r'\{\{format=%s\}\}[\s\S]+?\{\{end_format=%s\}\}' % (obj_type, obj_type))
            txt = pattern.sub('', txt)
            return txt

        def remove_marker(txt, obj_type):
            txt = txt.replace('{{format=%s}}' % obj_type, '')
            txt = txt.replace('{{end_format=%s}}' % obj_type, '')
            return txt

        all_formats = SerializeFormat.xml | SerializeFormat.json
        for format_code, format_string in SerializeFormat.get_all():
            if self.model.serialize_formats == all_formats:
                text = remove_content(text, format_string)
            else:
                if not (self.model.serialize_formats & format_code):
                    text = remove_content(text, format_string)
                else:
                    text = remove_marker(text, format_string)

        if self.model.serialize_formats != all_formats:
            text = remove_content(text, 'both')
        else:
            text = remove_marker(text, 'both')

        return text

    def prepare_file_codestype_php(self, text):
        text = WriterBase.prepare_file(self, text)
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
        return text
