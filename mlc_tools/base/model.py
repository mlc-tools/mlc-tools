import os
from copy import copy
from ..utils import fileutils
from ..utils.error import Log


class SerializeFormat(object):
    xml = 1
    json = 2

    @staticmethod
    def get_all():
        return (
            (SerializeFormat.xml, 'xml'),
            (SerializeFormat.json, 'json'),
        )


class Model(object):

    def __init__(self):
        self.parser = None

        self.classes = []
        self.classes_for_data = []
        self.objects = []
        self.functions = []
        self.classes_dict = {}

        self.model = None
        self.configs_directory = ''
        self.out_directory = ''
        self.data_directory = ''
        self.out_data_directory = ''
        self.language = 'py'
        self.only_data = False
        self.namespace = 'mg'
        self.side = 'both'
        self.php_validate = True
        self.test_script = ''
        self.test_script_args = ''
        self.generate_tests = False
        self.generate_intrusive = True
        self.generate_factory = True
        self.filter_code = None
        self.filter_data = None
        self.custom_generator = None
        self.additional_config_directories = []
        self.additional_data_directories = []
        self.serialize_protocol = []

        self.simple_types = ["int", "float", "bool", "string"]

        self.out_dict = None
        self.files = []
        self.created_files = []
        self.serialize_formats = SerializeFormat.xml | SerializeFormat.json

    def empty_copy(self):
        model = copy(self)
        model.classes = []
        model.classes_for_data = []
        model.objects = []
        model.functions = []
        model.classes_dict = {}
        return model

    def clear_data(self):
        self.parser = None
        self.classes = []
        self.classes_for_data = []
        self.objects = []
        self.functions = []
        self.classes_dict = {}
        self.out_dict = None
        self.files = []
        self.created_files = []

    def add_class(self, cls):
        self.classes_dict[cls.name] = cls
        self.classes.append(cls)

    def add_classes(self, classes):
        self.classes.extend(classes)
        for cls in classes:
            self.classes_dict[cls.name] = cls

    def get_class(self, name):
        return self.classes_dict[name]

    def has_class(self, name):
        return name in self.classes_dict

    def is_side(self, side):
        return self.side == 'both' or side == self.side or side == 'both'

    def is_lang(self, language):
        return not language or language == self.language

    def add_file(self, local_path, content):
        self.files.append((local_path, content))

    def save_files(self):
        if isinstance(self.out_dict, dict):
            for local_path, content in self.files:
                self.out_dict[local_path] = content
            return

        streams = []
        for local_path, content in self.files:
            self.created_files.append(local_path)
            full_path = fileutils.normalize_path(self.out_directory) + local_path
            exist = os.path.isfile(full_path)
            result, stream = fileutils.write(full_path, content)
            if result:
                streams.append(stream)
                msg = ' Create: {}' if not exist else ' Overwriting: {}'
                Log.debug(msg.format(local_path))
        for stream in streams:
            stream.close()

    def remove_old_files(self):
        files = fileutils.get_files_list(self.out_directory)
        for local_path in files:
            if local_path not in self.created_files and not local_path.endswith('.pyc'):
                os.remove(self.out_directory + local_path)
                Log.debug('Removed {}'.format(local_path))
