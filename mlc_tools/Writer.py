from . import fileutils
from .Object import *
from .Error import Log


def add_dict(inDict, toDict):
    for key in toDict:
        if key in inDict:
            inDict[key] += toDict[key]
        else:
            inDict[key] = toDict[key]
    return inDict


class Writer:

    def __init__(self, parser, serialize_format):
        self.parser = parser
        self.created_files = []
        self.simple_types = parser.simple_types
        self.serialize_format = serialize_format
        self.serialize_protocol = self.parser.serialize_protocol
        self.files = {}
        self.out_directory = ''
        self.current_class = None

    def convert_to_enum(self, cls, use_type='int'):
        shift = 0
        cast = use_type
        values = []
        for m in cls.members:
            if len(m.name):
                continue
            m.name = m.type
            m.type = cast
            m.is_static = True
            m.is_const = True
            if m.initial_value is None:
                if cast == 'int':
                    m.initial_value = '(1 << {})'.format(shift)
                    values.append(1 << shift)
                elif cast == 'string':
                    m.initial_value = '"{}"'.format(m.name)
            elif cast == 'int':
                # TODO if initialization is as enumerate of others members need throw error (example: one|two)
                values.append(m.initial_value)
            else:
                m.initial_value = 'None'

            shift += 1
        value = Object()
        value.initial_value = cls.members[0].name
        value.name = '_value'
        value.type = cast
        value.access = AccessSpecifier.private
        cls.members.append(value)
        return values

    def generate(self):
        self.write_classes(self.parser.classes, 0)

    def write_object(self, object_, flags):
        return {flags: ""}

    def write_class(self, class_, flags):
        return {flags: ""}

    def write_function(self, function, flags):
        return {flags: ""}

    def write_objects(self, objects, flags):
        out = {flags: '\n'}
        for object_ in objects:
            out = add_dict(out, self.write_object(object_, flags))
        return out

    def write_classes(self, classes, flags):
        for class_ in classes:
            if class_.type == 'enum':
                self.convert_to_enum(class_)
            if not class_.auto_generated:
                continue
            dictionary = self.write_class(class_, flags)
            filepath = self._get_filename_of_class(class_)
            self.files[filepath] = dictionary[flags]

    def write_functions(self, functions, flags):
        out = ''
        for function in functions:
            out += self.write_function(function, flags)
        return out

    def prepare_file(self, body):
        return body

    def save_file(self, filename, string):
        string = self.parser.copyright_text + self.prepare_file(string)
        filename = self.out_directory + filename
        self.created_files.append(filename)
        exist = fileutils.isfile(filename)
        if fileutils.write(filename, string):
            msg = ' Create: {}' if not exist else ' Overwriting: {}'
            Log.debug(msg.format(filename))

    def remove_non_actual_files(self):
        if not fileutils.isdir(self.out_directory):
            return
        files = fileutils.get_files_list(self.out_directory)
        for filename in files:
            if self.out_directory + filename not in self.created_files:
                if not filename.endswith('.pyc'):
                    Log.debug(' Removed: {}'.format(filename))
                fileutils.remove(self.out_directory + filename)

    def save_generated_classes(self, out_directory):
        self.out_directory = out_directory
        for file in self.files:
            self.save_file(file, self.files[file])

    def save_config_file(self):
        pass

    def _get_filename_of_class(self, class_):
        return class_.name

    def create_data_storage(self):
        pass
