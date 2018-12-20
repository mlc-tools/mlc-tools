

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

    def clear_data(self):
        self.parser = None
        self.classes = []
        self.classes_for_data = []
        self.objects = []
        self.functions = []
        self.classes_dict = {}

    def get_class(self, name):
        if name in self.classes_dict:
            return self.classes_dict[name]

        for cls in self.classes:
            if cls.name == name:
                self.classes_dict[name] = cls
                return cls
        return None

    def is_side(self, side):
        return self.side == 'both' or side == self.side or side == 'both'
