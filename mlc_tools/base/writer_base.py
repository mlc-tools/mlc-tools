import re
from .model import SerializeFormat
from ..core.object import AccessSpecifier


# pylint: disable=no-self-use
# pylint: disable=unused-argument
class WriterBase(object):

    def __init__(self, out_directory):
        self.model = None
        self.serializer = None
        self.out_directory = out_directory
        self.files = []
        self.created_files = []

    def save(self, model):
        self.model = model
        for cls in model.classes:
            if not cls.auto_generated:
                continue
            sources = self.write_class(cls)
            for filename, content in sources:
                self.model.add_file(filename, content)

    def write_class(self, cls):
        return [('', '')]

    def set_initial_values(self, cls):
        if cls.type == 'enum':
            for member in cls.members:
                if member.name == '_value' and member.initial_value is not None:
                    member.initial_value = cls.members[0].initial_value

    # Function methods
    def write_function(self, method):
        args = []
        if self.get_required_args_to_function(method) is not None:
            args.append(self.get_required_args_to_function(method))
        for name, arg in method.args:
            pattern = self.get_method_arg_pattern(arg)
            args.append(pattern.format(name, self.serializer.convert_initialize_value(arg.initial_value)))
        args = ', '.join(args)

        text = self.get_method_pattern().format(name=method.name,
                                                args=args,
                                                body=method.body,
                                                access=AccessSpecifier.to_string(method.access))
        if method.is_static:
            text = self.add_static_modifier_to_method(text)
        return text

    def get_method_arg_pattern(self, obj):
        return '${}={}' if obj.initial_value is not None else '${}'

    def get_method_pattern(self):
        return '{name}({args})\n{body}'

    def get_required_args_to_function(self, method):
        return None

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
