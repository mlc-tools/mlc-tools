import os
from ..utils import fileutils
from ..utils.error import Log


# pylint: disable=no-self-use
# pylint: disable=unused-argument
class WriterBase(object):

    def __init__(self, out_directory):
        self.model = None
        self.serializer = None
        self.out_directory = out_directory
        self.files = []
        self.created_files = []

    def save_file(self, filename, content):
        if self.model is not None and self.model.out_dict is not None:
            self.model.out_dict[filename] = content
            return

        full_path = fileutils.normalize_path(self.out_directory) + filename
        self.created_files.append(filename)
        exist = os.path.isfile(full_path)
        if fileutils.write(full_path, content):
            msg = ' Create: {}' if not exist else ' Overwriting: {}'
            Log.debug(msg.format(filename))

    def save(self, model):
        self.model = model
        for cls in model.classes:
            sources = self.write_class(cls)
            for filename, content in sources:
                self.save_file(filename, content)

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
                                                body=method.body)
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
        return text
