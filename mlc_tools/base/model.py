from copy import copy
from typing import List

from mlc_tools.core.class_ import Class


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

        self.classes:List[Class] = []
        self.classes_for_data = []
        self.objects = []
        self.functions = []
        self.classes_dict = {}
        self.includes = set()

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
        self.validate_allow_different_virtual_method = True
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
        self.join_to_one_file = False
        self.auto_registration = True
        self.generate_ref_counter = True
        self.user_includes = False
        self.empty_methods = False

        self.simple_types = ["int", "float", "bool", "string", 'int64_t', 'uint', 'unsigned', 'uint64_t', 'double']

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
        model.includes = set()
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
        return self.side == 'both' or side in [self.side, 'both']

    def is_lang(self, language):
        return not language or language == self.language

    def add_file(self, cls, local_path, content):
        self.files.append((cls, local_path, content))

    def get_subclasses_of_class(self, cls_name: str) -> List[Class]:
        result: List[Class] = []
        for cls in self.classes:
            if cls.superclasses and cls.superclasses[0] == cls_name:
                result.append(cls)
        return result
